use enigo::*;
use pyo3::prelude::*;

/// Parses a string representation of a key and returns the corresponding `Key` enum variant.
///
/// # Arguments
///
/// * `key` - A string slice that represents the key to be parsed.
///
/// # Returns
///
/// An `Option<Key>` that represents the corresponding `Key` enum variant if the parsing is successful, otherwise `None`.
/// NOTE: for a char key, even the input is upper case char, the returned value is still lower case.
fn parse(key: &str) -> Option<Key> {
    if key.len() == 1 && key.chars().all(|c| c.is_ascii_alphabetic()) {
        return Some(Key::Layout(
            key.chars().next().unwrap().to_ascii_lowercase(),
        ));
    }

    let lowercase_key = key.to_lowercase();
    match lowercase_key.as_str() {
        "capslock" => Some(Key::CapsLock),
        "shift" => Some(Key::Shift),
        "control" | "ctrl" => Some(Key::Control),
        "alt" => Some(Key::Alt),
        "super" | "meta" | "windows" | "win" | "cmd" => Some(Key::Meta),
        "backspace" => Some(Key::Backspace),
        "tab" => Some(Key::Tab),
        "return" | "enter" => Some(Key::Return),
        "escape" | "esc" => Some(Key::Escape),
        "delete" | "del" => Some(Key::Delete),
        "home" => Some(Key::Home),
        "end" => Some(Key::End),
        "pageup" => Some(Key::PageUp),
        "pagedown" => Some(Key::PageDown),
        "left" => Some(Key::LeftArrow),
        "right" => Some(Key::RightArrow),
        "up" => Some(Key::UpArrow),
        "down" => Some(Key::DownArrow),
        "f1" => Some(Key::F1),
        "f2" => Some(Key::F2),
        "f3" => Some(Key::F3),
        "f4" => Some(Key::F4),
        "f5" => Some(Key::F5),
        "f6" => Some(Key::F6),
        "f7" => Some(Key::F7),
        "f8" => Some(Key::F8),
        "f9" => Some(Key::F9),
        "f10" => Some(Key::F10),
        "f11" => Some(Key::F11),
        "f12" => Some(Key::F12),
        ";" => Some(Key::Layout(';')),
        "=" => Some(Key::Layout('=')),
        "," => Some(Key::Layout(',')),
        "-" => Some(Key::Layout('-')),
        "." => Some(Key::Layout('.')),
        "/" => Some(Key::Layout('/')),
        "`" => Some(Key::Layout('`')),
        "[" => Some(Key::Layout('[')),
        "\\" => Some(Key::Layout('\\')),
        "]" => Some(Key::Layout(']')),
        "'" => Some(Key::Layout('\'')),
        _ => None,
    }
}

#[pyfunction]
fn press(key: &str) {
    let mut enigo = Enigo::new();
    if let Some(key) = parse(key) {
        enigo.key_down(key);
    }
}

#[pyfunction]
fn release(key: &str) {
    let mut enigo = Enigo::new();
    if let Some(key) = parse(key) {
        enigo.key_up(key);
    }
}

#[pyfunction]
pub fn release_all() {
    let mut enigo = Enigo::new();
    for values in WIN_KEY_MAP.values() {
        let key = values.1;
        enigo.key_up(key);
    }
}

#[pyfunction]
fn tap(key: &str) {
    let mut enigo = Enigo::new();
    if let Some(key) = parse(key) {
        enigo.key_click(key);
    }
}

use enigo::{Enigo, KeyboardControllable};

use self::key_map::WIN_KEY_MAP;

mod key_map;
pub fn add_keyboard_funcs(m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(press, m)?)?;
    m.add_function(wrap_pyfunction!(release, m)?)?;
    m.add_function(wrap_pyfunction!(release_all, m)?)?;
    m.add_function(wrap_pyfunction!(tap, m)?)?;
    m.add_function(wrap_pyfunction!(key_map::get_pressed_key_strs, m)?)?;
    m.add_function(wrap_pyfunction!(key_map::get_pressed_key_index, m)?)?;

    Ok(())
}
