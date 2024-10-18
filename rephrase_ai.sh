#!/bin/bash

pkill torchrun 
torchrun --nproc_per_node 1 rephrase_ai.py
