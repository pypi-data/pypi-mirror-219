use enigo::{Enigo, MouseControllable};
use pyo3::prelude::*;

#[pyfunction]
pub fn move_to(x: usize, y: usize) {
    let mut enigo = Enigo::new();
    enigo.mouse_move_to(x as i32, y as i32);
}

#[pyfunction]
pub fn left_click() {
    let mut enigo = Enigo::new();
    enigo.mouse_click(enigo::MouseButton::Left);
}

#[pyfunction]
pub fn right_click() {
    let mut enigo = Enigo::new();
    enigo.mouse_click(enigo::MouseButton::Right);
}

#[pyfunction]
pub fn release_all() {
    let mut enigo = Enigo::new();
    enigo.mouse_up(enigo::MouseButton::Left);
    enigo.mouse_up(enigo::MouseButton::Right);
}

pub fn add_mouse_funcs(m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(move_to, m)?)?;
    m.add_function(wrap_pyfunction!(left_click, m)?)?;
    m.add_function(wrap_pyfunction!(right_click, m)?)?;

    Ok(())
}
