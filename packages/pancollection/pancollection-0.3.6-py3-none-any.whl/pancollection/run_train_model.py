# GPL License
# Copyright (C) UESTC
# All Rights Reserved
# @Author  : Xiao Wu
# @reference:
import torch
from udl_vis.mmcv.runner import Hook_v2, hooks, clip_grads
from udl_vis.AutoDL.base_runner import BaseRunner, detect_anomalous_parameters
# simplified hooks + base_runner + epoch_based_runner + trainer

class Trainer(BaseRunner, Hook_v2):

    def __init__(self, cfg, logger,
                 model, optimizer, scheduler,
                 hook={},
                 meta=None):
        super(Trainer, self).__init__(cfg, logger, model,
                                      optimizer, scheduler, hook, meta)

    def run_optimizer(self):

        self.optimizer.zero_grad()
        if self.detect_anomalous_params:
            detect_anomalous_parameters(self.model, self.outputs['loss'], self.logger)
        self.outputs['loss'].backward()
        if not hasattr(self.model, 'train'):
            grad_norm = clip_grads(self.grad_clip, self.model.model.parameters())
        else:
            grad_norm = clip_grads(self.grad_clip, self.model.parameters())

        self.log_buffer.update_dict({'grad_norm': float(grad_norm)})
        self.optimizer.step()




if __name__ == '__main__':
    from functools import partial
    from pancollection import TaskDispatcher, build_model, getDataSession
    from udl_vis.AutoDL.trainer import main

    arch = 'FusionNet'
    dataset_name = 'gf2'
    kwargs = dict(arch=arch, dataset_name=dataset_name, use_resume=False,
                      dataset={'train': 'gf2', 'valid': 'gf2', 'test': 'test_gf2_multiExm1.h5'},
                      workflow=[('train', 1)],  # ('valid', 1), ('test', 1),
                      resume_from=r"D:\Python\gitSync\UDL_package\PanCollection\results\pansharpening\gf2\FusionNet\Test\model_2023-06-25-12-20-04\1.pth.tar".replace('\\', '/'),
                      use_log_and_save=True, test='reduce')
    cfg = TaskDispatcher.new(task='pansharpening', mode='entrypoint', arch=kwargs.pop('arch'),
                             **kwargs)
    main(cfg, build_model, getDataSession, Trainer)

