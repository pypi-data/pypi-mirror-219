from PIL import Image

import torch
import time

from sdkit import Context
from sdkit.generate import generate_images
from sdkit.models import load_model
from sdkit.utils import diffusers_latent_samples_to_images, img_to_buffer, make_sd_context

from diffusers.pipelines.stable_diffusion import convert_from_ckpt
from diffusers.pipelines.stable_diffusion.convert_from_ckpt import (
    create_unet_diffusers_config,
    convert_ldm_unet_checkpoint,
    download_controlnet_from_original_ckpt,
)
from diffusers import StableDiffusionControlNetPipeline
from diffusers.models import ControlNetModel

from common import (
    TEST_DATA_FOLDER,
    get_image_for_device,
    get_tensor_for_device,
    assert_images_same,
    run_test_on_multiple_devices,
)

EXPECTED_DIR = f"{TEST_DATA_FOLDER}/expected_images/stable-diffusion"

context = None


# patch until https://github.com/huggingface/diffusers/pull/4119 is resolved
def convert_controlnet_checkpoint(
    checkpoint,
    original_config,
    checkpoint_path,
    image_size,
    upcast_attention,
    extract_ema,
    use_linear_projection=None,
    cross_attention_dim=None,
):
    ctrlnet_config = create_unet_diffusers_config(original_config, image_size=image_size, controlnet=True)
    ctrlnet_config["upcast_attention"] = upcast_attention

    ctrlnet_config.pop("sample_size")

    if use_linear_projection is not None:
        ctrlnet_config["use_linear_projection"] = use_linear_projection

    if cross_attention_dim is not None:
        ctrlnet_config["cross_attention_dim"] = cross_attention_dim

    # patch until https://github.com/huggingface/diffusers/pull/4119 is resolved
    x = dict(ctrlnet_config)
    del x["addition_embed_type"]
    del x["addition_time_embed_dim"]
    del x["transformer_layers_per_block"]
    # /patch

    controlnet_model = ControlNetModel(**x)

    # Some controlnet ckpt files are distributed independently from the rest of the
    # model components i.e. https://huggingface.co/thibaud/controlnet-sd21/
    if "time_embed.0.weight" in checkpoint:
        skip_extract_state_dict = True
    else:
        skip_extract_state_dict = False

    converted_ctrl_checkpoint = convert_ldm_unet_checkpoint(
        checkpoint,
        ctrlnet_config,
        path=checkpoint_path,
        extract_ema=extract_ema,
        controlnet=True,
        skip_extract_state_dict=skip_extract_state_dict,
    )

    controlnet_model.load_state_dict(converted_ctrl_checkpoint)

    return controlnet_model


convert_from_ckpt.convert_controlnet_checkpoint = convert_controlnet_checkpoint
# /patch


def canny(img: Image, thresholds=(100, 200)):
    import cv2
    import numpy as np

    img = np.array(img)
    img = cv2.Canny(img, *thresholds)
    img = img[:, :, None]
    img = np.concatenate([img, img, img], axis=2)
    img = Image.fromarray(img)
    return img


def pose(model, img: Image):
    return model(img)


def test_1_1__foo():
    from controlnet_aux.processor import Processor

    context = Context()
    context.test_diffusers = True
    context.model_paths["stable-diffusion"] = "models/stable-diffusion/aresMix_v01.safetensors"
    # context.model_paths["stable-diffusion"] = "models/stable-diffusion/official/2.1/v2-1_512-ema-pruned.safetensors"

    load_model(context, "stable-diffusion", enable_cache=False)

    pipe = context.models["stable-diffusion"]["default"]

    nets = [
        # ("scribble_hed", "control_v11p_sd15_scribble.pth", "control_v11p_sd15_scribble.yaml"),
        # ("softedge_hed", "control_v11p_sd15_softedge.pth", "control_v11p_sd15_softedge.yaml"),
        # ("scribble_hedsafe", "control_v11p_sd15_scribble.pth", "control_v11p_sd15_scribble.yaml"),
        # ("softedge_hedsafe", "control_v11p_sd15_softedge.pth", "control_v11p_sd15_softedge.yaml"),
        # ("depth_midas", "control_v11f1p_sd15_depth.pth", "control_v11f1p_sd15_depth.yaml"),
        # ("mlsd", "control_v11p_sd15_mlsd.pth", "control_v11p_sd15_mlsd.yaml"),
        # ("openpose", "control_v11p_sd15_openpose.pth", "control_v11p_sd15_openpose.yaml"),
        # ("openpose_face", "control_v11p_sd15_openpose.pth", "control_v11p_sd15_openpose.yaml"),
        # ("openpose_faceonly", "control_v11p_sd15_openpose.pth", "control_v11p_sd15_openpose.yaml"),
        # ("openpose_full", "control_v11p_sd15_openpose.pth", "control_v11p_sd15_openpose.yaml"),
        # ("openpose_hand", "control_v11p_sd15_openpose.pth", "control_v11p_sd15_openpose.yaml"),
        # ("scribble_pidinet", "control_v11p_sd15_scribble.pth", "control_v11p_sd15_scribble.yaml"),
        # ("softedge_pidinet", "control_v11p_sd15_softedge.pth", "control_v11p_sd15_softedge.yaml"),
        # ("scribble_pidsafe", "control_v11p_sd15_scribble.pth", "control_v11p_sd15_scribble.yaml"),
        # ("softedge_pidsafe", "control_v11p_sd15_softedge.pth", "control_v11p_sd15_softedge.yaml"),
        # ("normal_bae", "control_v11p_sd15_normalbae.pth", "control_v11p_sd15_normalbae.yaml"),
        # ("lineart_coarse", "control_v11p_sd15_lineart.pth", "control_v11p_sd15_lineart.yaml"),
        # ("lineart_realistic", "control_v11p_sd15_lineart.pth", "control_v11p_sd15_lineart.yaml"),
        # ("lineart_anime", "control_v11p_sd15s2_lineart_anime.pth", "control_v11p_sd15s2_lineart_anime.yaml"),
        # ("depth_zoe", "control_v11f1p_sd15_depth.pth", "control_v11f1p_sd15_depth.yaml"),
        # ("depth_leres", "control_v11f1p_sd15_depth.pth", "control_v11f1p_sd15_depth.yaml"),
        # ("depth_leres++", "control_v11f1p_sd15_depth.pth", "control_v11f1p_sd15_depth.yaml"),
        # ("shuffle", "control_v11e_sd15_shuffle.pth", "control_v11e_sd15_shuffle.yaml"),
        # ("canny", "control_v11p_sd15_canny.pth", "control_v11p_sd15_canny.yaml"),
        # ("segment", "control_v11p_sd15_seg.pth", "control_v11p_sd15_seg.yaml"),
        # ("ip2p", "control_v11e_sd15_ip2p.pth", "control_v11e_sd15_ip2p.yaml"),
        # ("canny", "control_v11p_sd21_canny.safetensors", "control_v11p_sd21_canny.yaml"),  # custom controlnet for SD 2
        # missing: tile, inpaint
    ]
    init_image = Image.open("out/xxx.jpg")

    from diffusers import UniPCMultistepScheduler

    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)

    for name, controlnet_path, controlnet_config_path in nets:
        controlnet_path = "models/controlnet/" + controlnet_path
        controlnet_config_path = "models/controlnet/" + controlnet_config_path

        t = time.time()
        if name == "segment":
            from controlnet_aux import SamDetector

            processor = SamDetector.from_pretrained("ybelkada/segment-anything", subfolder="checkpoints")
        elif name == "ip2p":
            processor = lambda x: x
        else:
            processor = Processor(name)
        print(name, "processor created in", (time.time() - t) * 1000, "ms")

        t = time.time()
        img = processor(init_image)
        print(name, "made image in", (time.time() - t) * 1000, "ms")
        img.save(f"out/pre_{name}.jpg")

        t = time.time()
        controlnet = download_controlnet_from_original_ckpt(
            controlnet_path, controlnet_config_path, from_safetensors=".safetensors" in controlnet_path, device="cpu"
        )
        print(name, "controlnet loaded in", (time.time() - t) * 1000, "ms")

        controlnet = controlnet.to(context.device, dtype=torch.float16 if context.half_precision else torch.float32)
        cn_pipe = StableDiffusionControlNetPipeline(controlnet=controlnet, **pipe.components)

        images = cn_pipe(
            prompt="Wonder Woman",
            negative_prompt="monochrome, lowres, bad anatomy, worst quality, low quality",
            image=img,
            num_inference_steps=20,
        ).images
        images[0].save(f"out/test_{name}.jpg")
