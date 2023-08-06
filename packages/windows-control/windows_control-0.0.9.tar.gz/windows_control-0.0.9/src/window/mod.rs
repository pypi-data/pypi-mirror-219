mod private;

// use image::{DynamicImage, GenericImageView};

use std::io::Cursor;

use pyo3::prelude::*;
use screenshots::Screen;

use winapi::shared::windef::HWND;

use image::DynamicImage;
use winapi::um::winuser::{
    GetForegroundWindow, IsIconic, SetForegroundWindow, SetWindowPos, ShowWindow,
};

#[pyclass]
struct Window {
    #[pyo3(get)]
    handle: usize,
}

#[pymethods]
impl Window {
    #[new]
    /// Creates a new `Window` instance with the specified `title` and `class`.
    /// If `title` or `class` are not specified, they should be set as `None` but not an empty string,
    /// because an empty string is still a valid value.
    fn new(title: Option<&str>, class: Option<&str>) -> Self {
        let hwnd = Window::get_window_handle(title, class);
        let handle = hwnd as usize;
        Window { handle }
    }

    /// acitivate the window, even it is minimized
    fn activate(&self) {
        unsafe {
            ShowWindow(self.handle as HWND, winapi::um::winuser::SW_RESTORE);
            SetForegroundWindow(self.handle as HWND);
        }
    }

    fn is_activated(&self) -> bool {
        // if is_minimized
        unsafe { GetForegroundWindow() == self.handle as HWND }
    }

    fn minimize(&self) {
        unsafe {
            ShowWindow(self.handle as HWND, winapi::um::winuser::SW_MINIMIZE);
            // NOTE: with the following line, self.is_minimized() will return false
            // ShowWindow(self.handle as HWND, winapi::um::winuser::SW_FORCEMINIMIZE);
        }
    }

    fn is_minimized(&self) -> bool {
        unsafe { IsIconic(self.handle as HWND) != 0 }
    }

    fn maximize(&self) {
        unsafe {
            ShowWindow(self.handle as HWND, winapi::um::winuser::SW_MAXIMIZE);
            SetForegroundWindow(self.handle as HWND);
        }
    }

    fn repos(&self, x: Option<i32>, y: Option<i32>) {
        let (x, y) = match (x, y) {
            (Some(x), Some(y)) => (x, y),
            (Some(x), None) => (x, self.get_pos().1),
            (None, Some(y)) => (self.get_pos().0, y),
            (None, None) => {
                panic!("At least one of x or y must be provided");
            }
        };

        unsafe {
            SetWindowPos(
                self.handle as HWND,
                winapi::um::winuser::HWND_TOP,
                x,
                y,
                0,
                0,
                winapi::um::winuser::SWP_FRAMECHANGED | winapi::um::winuser::SWP_NOSIZE,
            );
        }
    }

    fn resize(&self, width: Option<i32>, height: Option<i32>) {
        let (w, h) = match (width, height) {
            (Some(w), Some(h)) => (w, h),
            (Some(w), None) => (w, self.get_size().1),
            (None, Some(h)) => (self.get_size().0, h),
            (None, None) => {
                panic!("At least one of w or h must be provided");
            }
        };
        unsafe {
            SetWindowPos(
                self.handle as HWND,
                winapi::um::winuser::HWND_TOP,
                0,
                0,
                w,
                h,
                winapi::um::winuser::SWP_FRAMECHANGED | winapi::um::winuser::SWP_NOMOVE,
            );
        }
    }

    /// return the position of the window in (x, y) of the top left corner
    /// to that of the screen
    fn get_pos(&self) -> (i32, i32) {
        let rect = self.get_rect();
        (rect.0, rect.1)
    }

    /// return the size of the window in (width, height)
    fn get_size(&self) -> (i32, i32) {
        let rect = self.get_rect();
        (rect.2, rect.3)
    }

    // capture the screen only of the target window
    pub fn capture_screen(&self) -> Vec<u8> {
        let _start = std::time::Instant::now();
        let screen = Screen::all().unwrap()[0];

        // let mut image = screen.capture().unwrap(); // for global screen capture
        let pos = self.get_pos();
        let size = self.get_size();
        let image = screen
            .capture_area(pos.0, pos.1, size.0 as u32, size.1 as u32)
            .unwrap();

        // println!("screen display info:{:?}", screen.display_info.id);
        // std::fs::write(format!("./{}.png", screen.display_info.id), buffer).unwrap();

        image.to_png().unwrap()
    }

    fn record(&self, show: bool) {
        println!("start record");
        let screen_shot = self.capture_screen();
        // Convert the screen shot to a DynamicImage object
        let mut cursor = Cursor::new(screen_shot);
        let _img: DynamicImage = image::load(&mut cursor, image::ImageFormat::Png).unwrap();

        // Show the image if requested
        if show {
            // let (width, height) = img.dimensions();
            // TODO:
            // my_show_image::my_show_image(&img /* , width as i32, height as i32 */);
        }

        println!("end record");
    }
}

// add the class from this `mod.rs` to root python module
pub fn add_window_class(m: &PyModule) -> PyResult<()> {
    m.add_class::<Window>()?;
    Ok(())
}
//↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓other useful funcs↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
fn hwnd_to_dec_str(hwnd: HWND) -> usize {
    usize::from_str_radix(format!("{:?}", hwnd).trim_start_matches("0x"), 16).unwrap()
}
//↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑other useful funcs↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

pub fn add_window_funcs(_m: &PyModule) -> PyResult<()> {
    // m.add_function(wrap_pyfunction!(open_app, m)?)?;
    Ok(())
}
