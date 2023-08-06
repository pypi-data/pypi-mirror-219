
'''
path_list=( /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_10g_bnkps.v8.trt \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_10g.v8.trt \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_500m_bnkps.v8.trt \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_500m.v8.trt \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_r50_insightface.v8.trt \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_torch_r50.v8.trt \
            /data/notebook/NAS/FaceDetection/models/retinaface-mobileNet/retinaface_mnet.25.v8.trt \

            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_10g_bnkps.vino \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_10g.vino \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_500m_bnkps.vino \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_500m.vino \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_r50_insightface.vino \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_torch_r50.vino \
            /data/notebook/NAS/FaceDetection/models/retinaface-mobileNet/retinaface_mnet.25.vino \

            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_10g_bnkps.onnx \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_10g.onnx \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_500m_bnkps.onnx \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_500m.onnx \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_r50_insightface.onnx \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_torch_r50.onnx \
            /data/notebook/NAS/FaceDetection/models/retinaface-mobileNet/retinaface_mnet.25.onnx

)

name_list=( scrfd scrfd scrfd scrfd retinaface_insightface retinaface_torch retinaface_insightface \
            scrfd scrfd scrfd scrfd retinaface_insightface retinaface_torch retinaface_insightface \
            scrfd scrfd scrfd scrfd retinaface_insightface retinaface_torch retinaface_insightface )

save_name=( scrfd_10g_bnkps.v8.trt \
            scrfd_10g.v8.trt \
            scrfd_500m_bnkps.v8.trt \
            scrfd_500m.v8.trt \
            retinaface_r50_insightface.v8.trt \
            retinaface_torch_r50.v8.trt \
            retinaface_mnet.25.trt \

            scrfd_10g_bnkps.vino \
            scrfd_10g.vino \
            scrfd_500m_bnkps.vino \
            scrfd_500m.vino \
            retinaface_r50_insightface.vino \
            retinaface_torch_r50.vino \
            retinaface_mnet.25.vino \

            scrfd_10g_bnkps.onnx \
            scrfd_10g.onnx \
            scrfd_500m_bnkps.onnx \
            scrfd_500m.onnx \
            retinaface_r50_insightface.onnx \
            retinaface_torch_r50.onnx \
            retinaface_mnet.25.onnx
)

# singlescale, only cuda onnx
for (( i = 0 ; i < 21 ; i++ )) ; do
    echo "get widerface ${path_list[$i]}"
    python -u get_widerface_txt.py \
    --dt_name ${name_list[$i]} \
    --dt_path ${path_list[$i]} \
    --save_format result_txt_220513_all/${save_name[$i]}
    
    echo "eval widerface ${path_list[$i]}"
    python -u eval_widerface.py \
    --dt_name ${name_list[$i]} \
    --dt_path ${path_list[$i]} \
    --pred_format result_txt_220513_all/${save_name[$i]} \
    --save_format result_pkl_220513_all/${save_name[$i]}.pkl
    echo "finish"

done

echo "Start onnx cpu"
path_list=( 
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_10g_bnkps.onnx \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_10g.onnx \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_500m_bnkps.onnx \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/scrfd_500m.onnx \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_r50_insightface.onnx \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_torch_r50.onnx \
            /data/notebook/NAS/FaceDetection/models/retinaface-mobileNet/retinaface_mnet.25.onnx
)

name_list=( scrfd scrfd scrfd scrfd retinaface_insightface retinaface_torch retinaface_insightface )

save_name=( scrfd_10g_bnkps.onnx \
            scrfd_10g.onnx \
            scrfd_500m_bnkps.onnx \
            scrfd_500m.onnx \
            retinaface_r50_insightface.onnx \
            retinaface_torch_r50.onnx \
            retinaface_mnet.25.onnx
)
# onnx cpu
for (( i = 0 ; i < 7 ; i++ )) ; do
    echo "get widerface ${path_list[$i]}"
    python -u get_widerface_txt.py \
    --dt_name ${name_list[$i]} \
    --dt_path ${path_list[$i]} \
    --save_format result_txt_220513_all/${save_name[$i]}_cpu \
    --onnx_cpu
    
    echo "eval widerface ${path_list[$i]}"
    python -u eval_widerface.py \
    --dt_name ${name_list[$i]} \
    --dt_path ${path_list[$i]} \
    --pred_format result_txt_220513_all/${save_name[$i]}_cpu \
    --save_format result_pkl_220513_all/${save_name[$i]}_cpu.pkl 
    echo "finish"

done


echo "Start multiscale retinaface"

echo "get widerface retinaface torch multiple trt"
python -u get_widerface_txt.py \
--dt_name retinaface_torch \
--dt_path /data/notebook/NAS/FaceDetection/models/retinaface_torch/retinaface_r50_final_multiple.v8.trt \
--save_format result_txt_220513_all/retinface_torch_multiple.trt \
--load_multi \
--multiscale
echo "eval widerface retinaface torch multiple trt"
python -u eval_widerface.py \
--dt_name retinaface_torch \
--dt_path /data/notebook/NAS/FaceDetection/models/retinaface_torch/retinaface_r50_final_multiple.v8.trt \
--pred_format result_txt_220513_all/retinface_torch_multiple.trt \
--save_format result_pkl_220513_all/retinface_torch_multiple.trt.pkl 



echo "get widerface retinaface torch multiple onnx cpu"
python -u get_widerface_txt.py \
--dt_name retinaface_torch \
--dt_path /data/notebook/NAS/FaceDetection/models/retinaface_torch/retinaface_r50_final_multiple.onnx \
--save_format result_txt_220513_all/retinface_torch_multiple.onnx_cpu \
--multiscale \
--onnx_cpu
echo "eval widerface retinaface torch multiple onnx cpu"
python -u eval_widerface.py \
--dt_name retinaface_torch \
--dt_path /data/notebook/NAS/FaceDetection/models/retinaface_torch/retinaface_r50_final_multiple.onnx \
--pred_format result_txt_220513_all/retinface_torch_multiple.onnx_cpu \
--save_format result_pkl_220513_all/retinface_torch_multiple.onnx_cpu.pkl 

echo "get widerface retinaface torch multiple onnx cuda"
python -u get_widerface_txt.py \
--dt_name retinaface_torch \
--dt_path /data/notebook/NAS/FaceDetection/models/retinaface_torch/retinaface_r50_final_multiple.onnx \
--save_format result_txt_220513_all/retinface_torch_multiple.onnx \
--multiscale
echo "eval widerface retinaface torch multiple onnx cuda"
python -u eval_widerface.py \
--dt_name retinaface_torch \
--dt_path /data/notebook/NAS/FaceDetection/models/retinaface_torch/retinaface_r50_final_multiple.onnx \
--pred_format result_txt_220513_all/retinface_torch_multiple.onnx \
--save_format result_pkl_220513_all/retinface_torch_multiple.onnx.pkl 


path_list=( 
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_r50_insightface.vino \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_r50_insightface.onnx \
            /data/notebook/NAS/PTAS_Shared/resource/model/face/detection/retinaface_r50_insightface.v8.trt \
            /data/notebook/NAS/FaceDetection/models/retinaface-mobileNet/retinaface_mnet.25.vino \
            /data/notebook/NAS/FaceDetection/models/retinaface-mobileNet/retinaface_mnet.25.onnx \
            /data/notebook/NAS/FaceDetection/models/retinaface-mobileNet/retinaface_mnet.25.v8.trt
)

name_list=( retinaface_insightface retinaface_insightface retinaface_insightface \
            retinaface_insightface retinaface_insightface retinaface_insightface)

# singlescale, only cuda onnx
for (( i = 0 ; i < 6 ; i++ )) ; do
    echo "get widerface ${path_list[$i]}"
    python -u get_widerface_txt.py \
    --dt_name ${name_list[$i]} \
    --dt_path ${path_list[$i]} \
    --save_format result_txt_220517_retest/${save_name[$i]}
    
    echo "eval widerface ${path_list[$i]}"
    python -u eval_widerface.py \
    --dt_name ${name_list[$i]} \
    --dt_path ${path_list[$i]} \
    --pred_format result_txt_220517_retest/${save_name[$i]} \
    --save_format result_pkl_220517_retest/${save_name[$i]}.pkl
    echo "finish"

done

'''

'''
echo "Start ETRI model test"
for (( i = 600 ; i <= 1000 ; i+=10 )) ; do
    echo "start $i"

    python -u get_widerface_txt.py \
    --dt_name retinaface_torch \
    --dt_path /data/notebook/yoonms/frvt_test/models/fle_model/r50_retinaface_onnx/dynamic_model_opset11.onnx \
    --save_format result_txt_220613_inputIter/retinaface_etri_op11.onnx_pad_input$i \
    --input_size $i $i \
    --resize_way pad

    python -u eval_widerface.py \
    --dt_name retinaface_torch \
    --dt_path /data/notebook/yoonms/frvt_test/models/fle_model/r50_retinaface_onnx/dynamic_model_opset11.onnx \
    --pred_format result_txt_220613_inputIter/retinaface_etri_op11.onnx_pad_input$i \
    --save_format result_pkl_220613_inputIter/retinaface_etri_op11.onnx_pad_input$i.pkl

done
'''

echo "Start Our model test - multiscale"
for (( i = 300 ; i <= 1000 ; i+=10 )) ; do
    echo "start $i"

    python -u get_widerface_txt.py \
    --dt_name retinaface_torch \
    --dt_path /data/notebook/NAS/FaceDetection/models/retinaface_torch/retinaface_r50_final_multiple.onnx \
    --save_format result_txt_220614_targetIter/retinaface_torch_r50_own_dynamic.onnx_multiscale_target$i \
    --target_size $i \
    --max_size 1200 \
    --multiscale \
    --write_time

    python -u eval_widerface.py \
    --dt_name retinaface_torch \
    --dt_path /data/notebook/NAS/FaceDetection/models/retinaface_torch/retinaface_r50_final_multiple.onnx \
    --pred_format result_txt_220614_targetIter/retinaface_torch_r50_own_dynamic.onnx_multiscale_target$i \
    --save_format result_pkl_220614_targetIter/retinaface_torch_r50_own_dynamic.onnx_multiscale_target$i.pkl

done