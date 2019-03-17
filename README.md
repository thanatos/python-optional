The classic `Option` class — a class whose instances represent either some
value, or nothing — for Python.

This class is modeled after the Rust `Option` type, and provides many of the
same helper methods, such as `map` and `unwrap`.

# What about `None`?

`None` works well for many cases. However, sometimes, one needs to indicate
that the enclosed value might itself be `None` (often in generic cases); `None`
offers us no way of representing `Some(None)`, because we lack the `Some(...)`
side.
