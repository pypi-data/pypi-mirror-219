use pyo3::prelude::*;
mod clean_up;
mod keyboard;
mod mouse;
mod window;

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn windows_control(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    // Add your module's functions here
    // Register the cleanup function
    unsafe {
        pyo3::ffi::Py_AtExit(Some(clean_up::get_cleanup_function()));
    }

    // Import funcs
    // m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    // m.add_function(wrap_pyfunction!(test_opencv, m)?)?;

    // import sub modules
    register_keyboard_sub_module(py, m)?;
    register_mouse_sub_module(py, m)?;
    register_window_sub_module(py, m)?;

    Ok(())
}

fn register_keyboard_sub_module(py: Python<'_>, parent_module: &PyModule) -> PyResult<()> {
    let child_module = PyModule::new(py, "keyboard")?;
    keyboard::add_keyboard_funcs(child_module)?;
    parent_module.add_submodule(child_module)?;

    Ok(())
}

fn register_mouse_sub_module(py: Python<'_>, parent_module: &PyModule) -> PyResult<()> {
    let child_module = PyModule::new(py, "mouse")?;
    mouse::add_mouse_funcs(child_module)?;
    parent_module.add_submodule(child_module)?;

    Ok(())
}

fn register_window_sub_module(py: Python<'_>, parent_module: &PyModule) -> PyResult<()> {
    let child_module = PyModule::new(py, "window")?;
    window::add_window_class(child_module)?;
    window::add_window_funcs(child_module)?;
    parent_module.add_submodule(child_module)?;

    Ok(())
}
