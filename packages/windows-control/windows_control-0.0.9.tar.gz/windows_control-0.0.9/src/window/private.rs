use std::ffi::OsStr;
use std::os::windows::prelude::OsStrExt;
use std::ptr::null_mut;

use winapi::shared::windef::{HWND, POINT, RECT};

use winapi::um::winuser::{ClientToScreen, GetClientRect};

use super::Window;

// this block lists non-pub methods

impl Window {
    pub fn get_window_handle(title: Option<&str>, class: Option<&str>) -> HWND {
        let title_ptr = match title {
            // NOT OK: Some(t) => t.encode_utf16().collect::<Vec<u16>>().as_ptr(),
            Some(t) => OsStr::new(t)
                .encode_wide()
                .chain(Some(0).into_iter())
                .collect::<Vec<_>>()
                .as_ptr(),
            None => null_mut(),
        };
        let class_ptr = match class {
            // NOT OK: Some(c) => c.encode_utf16().collect::<Vec<u16>>().as_ptr(),
            Some(c) => OsStr::new(c)
                .encode_wide()
                .chain(Some(0).into_iter())
                .collect::<Vec<_>>()
                .as_ptr(),
            None => null_mut(),
        };

        if title_ptr.is_null() && class_ptr.is_null() {
            panic!("At least one of title or class_name must be provided");
        }

        // way1: classic find window
        let hwnd = unsafe { winapi::um::winuser::FindWindowW(class_ptr, title_ptr) };
        // way2: with child found feature
        // let mut child = null_mut();
        // let mut hwnd = null_mut();
        // unsafe {
        //     let _child = winapi::um::winuser::FindWindowExW(hwnd, child, class_ptr, title_ptr);
        // };
        println!(
            "the found window handle is: {hwnd:?} ({})",
            Window::hwnd_to_dec_str(hwnd)
        );

        hwnd
    }

    fn hwnd_to_dec_str(hwnd: HWND) -> usize {
        usize::from_str_radix(format!("{:?}", hwnd).trim_start_matches("0x"), 16).unwrap()
    }

    pub fn get_rect(&self) -> (i32, i32, i32, i32) {
        let mut rect = RECT {
            left: 0,
            top: 0,
            right: 0,
            bottom: 0,
        };
        unsafe {
            GetClientRect(self.handle as HWND, &mut rect);
            // x, y
            let mut point = POINT {
                x: rect.left,
                y: rect.top,
            };
            ClientToScreen(self.handle as HWND, &mut point);
            rect.left = point.x;
            rect.top = point.y;
            // right, right
            let mut bottom_right = POINT {
                x: rect.right,
                y: rect.bottom,
            };
            ClientToScreen(self.handle as HWND, &mut bottom_right);
            rect.right = bottom_right.x;
            rect.bottom = bottom_right.y;
        }

        let width = rect.right - rect.left;
        let height = rect.bottom - rect.top;
        let x = rect.left;
        let y = rect.top;

        (x, y, width, height)
    }
}
