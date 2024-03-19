use lopdf::Document;
use pyo3::prelude::*;

fn extract_text_from_pdf(pdf_bytes: &[u8]) -> Result<String, lopdf::Error> {
    match Document::load_mem(pdf_bytes) {
        Ok(doc) => {
            let mut text = String::new();
            let pages = doc.get_pages();
            for (i, _) in pages.iter().enumerate() {
                let page_number = (i + 1) as u32;
                text.push_str(&doc.extract_text(&[page_number]).unwrap_or_default());
            }
            Ok(text)
        }
        Err(e) => Err(e),
    }
}

#[pyfunction]
fn process_pdf(_py: Python, pdf_bytes: &[u8]) -> PyResult<String> {
    match extract_text_from_pdf(pdf_bytes) {
        Ok(text) => Ok(text),
        Err(_) => Ok("error".to_string()),
    }
}

#[pymodule]
fn pdf_processor(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(process_pdf))?;
    Ok(())
}
