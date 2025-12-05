from typing import Optional
import numpy as np

def align_by_si_lsq(src: np.ndarray, tgt: np.ndarray, mask: Optional[np.ndarray]=None):
    if mask is None:
        st = np.sum(src * tgt)
        s2 = np.sum(src * src)
    else:
        M = mask.sum()
        st = np.sum(src * tgt * mask) / M
        s2 = np.sum(src * src * mask) / M
    scale = st / s2
    src = src * scale
    return src, (scale, 0)

def align_by_ssi_lsq(src: np.ndarray, tgt: np.ndarray, mask: Optional[np.ndarray]=None):
    if mask is None:
        src_avg = src.mean()
        tgt_avg = tgt.mean()
        s_t_avg = np.mean(src * tgt)
        s_s_avg = np.mean(src * src)

    else:
        M = mask.sum()
        src_avg = np.sum(src * mask) / M
        tgt_avg = np.sum(tgt * mask) / M
        s_t_avg = np.sum(src * tgt * mask) / M
        s_s_avg = np.sum(src * src * mask) / M

    D = s_s_avg - src_avg * src_avg
    scale = (s_t_avg - src_avg * tgt_avg) / D
    shift = (s_s_avg * tgt_avg - src_avg * s_t_avg) / D
    src = src * scale + shift
    return src, (scale, shift)
