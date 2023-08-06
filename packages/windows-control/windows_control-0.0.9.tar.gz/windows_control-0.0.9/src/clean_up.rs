use lazy_static::lazy_static;
use std::sync::Once;

use crate::{keyboard, mouse};

static INIT: Once = Once::new();

lazy_static! {
    static ref CLEANUP_FUNCTION: extern "C" fn() = {
        INIT.call_once(|| {
            // Your cleanup function initialization code here
        });

        // Return your cleanup function
        extern "C" fn cleanup() {
            keyboard::release_all();
            mouse::release_all();
            println!("Cleaning up...");
        }

        cleanup
    };
}

pub fn get_cleanup_function() -> extern "C" fn() {
    *CLEANUP_FUNCTION
}
