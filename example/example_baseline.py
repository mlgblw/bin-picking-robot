"""
Exp mode for three methods
0 -> FGE (Graspability)
1 -> EMap
2 -> PN
"""
import argparse
from bpbot.binpicking import *

def detect(img_path, exp_mode):
    h_params = {
        "finger_length": 15,
        "finger_width":  8, 
        "open_width":    40
    }
    # h_params = {
    #     "finger_length": 15,
    #     "finger_width":  8, 
    #     "open_width":    30
    # }
    g_params = {
        "rotation_step": 22.5, 
        "depth_step":    50,
        "hand_depth":    50
    }
    t_params = {
        "compressed_size": 250,
        "len_thld": 15,
        "dist_thld": 3,
        "sliding_size": 125,
        "sliding_stride": 25
    }
    print(f"[*] Method : {exp_mode}")
    if exp_mode.lower() == "fge":
        grasps = detect_grasp(n_grasp=1, img_path=img_path, 
                        g_params=g_params,
                        h_params=h_params)
        print("test:", grasps)
        if grasps is not None: 
            return grasps[0][:2]
        return

    elif exp_mode.lower() == "emap": 
        grasps = detect_nontangle_grasp(n_grasp=1, img_path=img_path, 
                                    g_params=g_params, 
                                    h_params=h_params,
                                    t_params=t_params)
        if grasps is not None: 
            return grasps[0][:2]
        return
    
    elif exp_mode.lower() == "pn":
        from bpbot.module_picksep import PickSepClient
        psc = PickSepClient()
        ret = psc.infer_picknet(img_path)
        return ret[1][:2]
    else: 
        print("[!] No valid mode! ")
        return

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str, help="Exp mode => [FGE, EMap, PN]")
    
    args = parser.parse_args()

    img_path = "C:\\Users\\xinyi\\Documents\\XYBin_Pick\\bin\\tmp\\depth.png"
    txt_path = "C:\\Users\\xinyi\\Documents\\XYBin_Pick\\bin\\tmp\\grasp.txt"
    g = detect(img_path, args.mode)
    print(g)
    if g is not None: 
        with open(txt_path, 'w') as fp:
            if g is not None: 
                print(f"{int(g[0])} {int(g[1])}", file=fp)
            else: 
                print("0 0", file=fp)
        from datetime import datetime as dt
        tdatetime = dt.now()
        tstr = tdatetime.strftime("%Y%m%d%H%M%S")
        save_path = os.path.join("C:\\Users\\xinyi\\Documents\\XYBin_Collected\\exp_picksim", tstr+".png")
        # ----------- PN save -------------
        # out = cv2.imread("C:\\Users\\xinyi\\Documents\\XYBin_Pick\\bin\\tmp\\pred\\out_depth.png")
        # ret = cv2.imread("C:\\Users\\xinyi\\Documents\\XYBin_Pick\\bin\\tmp\\pred\\ret_depth.png")
        # cv2.imwrite(save_path, cv2.hconcat((out, ret)))

        # ----------- FGE/EMap save -------------
        img = cv2.imread(img_path)
        cv2.circle(img, (int(g[0]),int(g[1])), 7, (0,255,0), -1)
        cv2.imwrite(save_path, img)
        print("[*] Save in ", save_path)
    else: 
        print("[!] Failed! ")
        
        