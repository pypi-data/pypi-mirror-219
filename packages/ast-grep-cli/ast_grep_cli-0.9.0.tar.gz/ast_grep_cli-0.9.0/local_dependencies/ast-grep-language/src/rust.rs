use crate::parsers::language_rust;
use ast_grep_core::language::{Language, TSLanguage};
use std::borrow::Cow;

// impl_lang!(Rust, language_rust);
#[derive(Clone, Copy)]
pub struct Rust;
impl Language for Rust {
  fn get_ts_language(&self) -> TSLanguage {
    language_rust()
  }
  // we can use any char in unicode range [:XID_Start:]
  // https://doc.rust-lang.org/reference/identifiers.html
  fn expando_char(&self) -> char {
    'µ'
  }
  fn pre_process_pattern<'q>(&self, query: &'q str) -> Cow<'q, str> {
    // use stack buffer to reduce allocation
    let mut buf = [0; 4];
    let expando = self.expando_char().encode_utf8(&mut buf);
    // TODO: use more precise replacement
    let replaced = query.replace(self.meta_var_char(), expando);
    Cow::Owned(replaced)
  }
}

#[cfg(test)]
mod test {
  use super::*;
  use ast_grep_core::{source::TSParseError, Matcher, Pattern};

  fn test_match(s1: &str, s2: &str) {
    let pattern = Pattern::str(s1, Rust);
    let cand = Rust.ast_grep(s2);
    assert!(
      pattern.find_node(cand.root()).is_some(),
      "goal: {:?}, candidate: {}",
      pattern,
      cand.root().to_sexp(),
    );
  }

  #[test]
  fn test_rust_pattern() {
    // fix #6
    test_match("Some($A)", "fn test() { Some(123) }");
    test_match(
      "
match $A {
    Some($B) => $B,
    None => $C,
}",
      r#"fn test() {
patterns = match config.include.clone() {
    Some(patterns) => patterns,
    None => Vec::from([cwd
        .join("**/*.toml")
        .normalize()
        .to_string_lossy()
        .into_owned()]),
};
}"#,
    );
  }

  #[test]
  fn test_rust_wildcard_pattern() {
    // fix #412
    test_match("|$A, $B|", "let w = v.into_iter().reduce(|x, y| x + y);");
    test_match("|$$A, $$B|", "let w = v.into_iter().reduce(|x, _| x + x);");
    test_match("let ($$X, $$Y) = $$$T;", "let (_, y) = (1, 2);");
  }

  #[test]
  fn test_rust_spread_syntax() {
    test_match(
      "let ($X, $Y) = $$$T;",
      "let (.., y) = (1,2,3,4,5,6,7,8,9,10);",
    );
    test_match(
      "$C { $$$A, ..$B};",
      r#"User { 
      username: String::from(name),
      ..DEFAULT_USER 
    };"#,
    );
  }

  fn test_replace(src: &str, pattern: &str, replacer: &str) -> Result<String, TSParseError> {
    let mut source = Rust.ast_grep(src);
    let replacer = Pattern::new(replacer, Rust);
    assert!(source.replace(pattern, replacer)?);
    Ok(source.generate())
  }

  #[test]
  fn test_rust_replace() -> Result<(), TSParseError> {
    let ret = test_replace("fn test() { Some(123) }", "Some($A)", "Ok($A)")?;
    assert_eq!(ret, "fn test() { Ok(123) }");
    let ret = test_replace(
      r#"
patterns = match config.include.clone() {
    Some(patterns) => patterns,
    None => 123,
}"#,
      "match $A {
    Some($B) => $B,
    None => $C,
}",
      "$A.unwrap_or($C)",
    )?;
    assert_eq!(ret, "\npatterns = config.include.clone().unwrap_or(123)");
    Ok(())
  }
}
