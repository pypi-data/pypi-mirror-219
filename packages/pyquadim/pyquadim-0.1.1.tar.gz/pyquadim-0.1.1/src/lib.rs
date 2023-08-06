use csscolorparser::Color;
use image::{ImageBuffer, Rgba};
use pyo3::prelude::*;
use quadim::{AnalyzeParams, ClassicBrush, GenericParams, MergeMethod, PixelType, RenderParams, SampleType};

fn parse_color(color: &str, default: Color) -> PixelType {
    PixelType::from(csscolorparser::parse(color).unwrap_or(default).to_rgba8())
}

#[pyfunction]
#[pyo3(signature = (
im,
width,
height,
ratio = (1, 1),
depth = 8,
thres_ay = 20.,
thres_cbcr = 2.,
merge_method = "stdev",
bg_color = "white",
stroke_color = "black",
stroke_width = 0,
seed = 0,
shape = "rect"
))]
fn render(
    im: Vec<(u8, u8, u8, u8)>,
    width: u32,
    height: u32,
    ratio: (u8, u8),
    depth: u8,
    thres_ay: f32,
    thres_cbcr: f32,
    merge_method: &str,
    bg_color: &str,
    stroke_color: &str,
    stroke_width: u32,
    seed: u64,
    shape: &str,
) -> PyResult<Vec<(u8, u8, u8, u8)>> {
    let mut img = ImageBuffer::from_fn(width, height, |x, y| {
        let (r, g, b, a) = im[(y * width + x) as usize];
        Rgba([r, g, b, a])
    });

    let mut canvas = vec![(0u8, SampleType::zeros()); 7680 * 4320].into_boxed_slice();

    let ge_params = GenericParams {
        slicing_ratio: ratio,
        max_depth: depth,
    };

    let an_params = AnalyzeParams {
        thres_ay,
        thres_cbcr,
        merge_method: match merge_method {
            "range" => MergeMethod::Range,
            "stdev" => MergeMethod::StDev,
            &_ => MergeMethod::StDev
        },
    };

    let re_params = RenderParams {
        bg_color: parse_color(bg_color, Color::new(1f64, 1f64, 1f64, 1f64)),
        stroke_color: parse_color(stroke_color, Color::new(0f64, 0f64, 0f64, 1f64)),
        stroke_width,
        seed,
    };

    let brush = Box::from(match shape {
        "rect" => ClassicBrush::Rect,
        "circle" => ClassicBrush::Circle,
        "cross" => ClassicBrush::Cross,
        "yr-add" => ClassicBrush::YrAdd,
        "yr-mul" => ClassicBrush::YrMul,
        &_ => ClassicBrush::Rect
    });

    quadim::analyze(&img, &mut canvas, ge_params, an_params)
        .expect("[pyquadim] image analyze failed!");
    quadim::render(&mut img, &canvas, brush, ge_params, re_params, 0f32)
        .expect("[pyquadim] image render failed!");

    let mut ret = Vec::<(u8, u8, u8, u8)>::with_capacity((width * height) as usize);
    for y in 0..height {
        for x in 0..width {
            let pix = img.get_pixel(x, y);
            ret.push((pix[0], pix[1], pix[2], pix[3]));
        }
    }

    Ok(ret)
}

#[pymodule]
fn pyquadim(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(render, m)?)?;
    Ok(())
}