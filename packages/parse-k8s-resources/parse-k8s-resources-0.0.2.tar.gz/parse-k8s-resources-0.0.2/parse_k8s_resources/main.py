#!/usr/bin/env python
# coding:utf-8

"""
@Time : 2023/7/13 15:43 
@Author : harvey
@File : main.py 
@Software: PyCharm
@Desc: 
@Module
"""

import argparse
import json
import os.path
import sys

import prettytable as pt
from tabulate import tabulate

tb = pt.PrettyTable()
tb_sum = pt.PrettyTable()


def get_args():
    parser = argparse.ArgumentParser(
        prog='parse_deployment_resource',
        description="Statistics k8s deployment/statefulset memory and cpu.==>>"
                    "example：kubectl get deployment -A -o json| parse_k8s_resources",
    )
    parser.add_argument('-f', dest='jsonfile', help="k8s json file path", required=False)
    parser.add_argument('--fmt', dest='fmt', default='simple', help="simple|grid|github", required=False)
    args = parser.parse_args()
    if args.jsonfile and not os.path.exists(args.jsonfile):
        print("error, %s is not exists" % args.jsonfile)
        sys.exit()
    return args


def unit_trans_memory(original):
    if original == 0:
        return 0
    original = original.strip()
    unit_list = [("Gi", 1024 * 1024), ("Mi", 1024,), ("m", 1024), ]
    for i in unit_list:
        tmp_list = original.split(i[0])
        if len(tmp_list) == 2:
            if tmp_list[1] != "":
                raise Exception("单位错误")
            return int(tmp_list[0]) * i[1]
    return 0


def unit_trans_cpu(original):
    if not original:
        return 0
    original = str(original).strip()
    if not original.endswith('m'):
        return float(original)
    return float(original.split('m')[0]) / 1000


def read_resource_data():
    """从文件获取或从标准输入获取"""
    args = get_args()
    if not sys.stdin.isatty():
        # 存在管道输入
        data = sys.stdin.read()
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            print("请输出json格式，示例：kubectl get deployments -A -o json | parse-k8s-resources")
    filename = args.jsonfile
    if not filename:
        print("pipeline input and jsonfile not defined")
        sys.exit()
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def print_dp_memory():
    args = get_args()
    count = 0
    sum_mem_request_bytes = 0
    sum_mem_limit_bytes = 0
    sum_cpu_request_float = 0
    sum_cpu_limit_float = 0
    data = read_resource_data()
    id = 0
    table_data = []
    kind = ''
    for dp in data.get('items'):
        name = dp.get('metadata').get('name')
        kind = dp.get('kind')
        namespace = dp.get('metadata').get('namespace')
        generation = dp.get('metadata').get('generation')
        replicas = dp.get('status').get('replicas', 0)
        if replicas == 0:
            continue
        id += 1
        container_count = len(dp.get('spec').get('template').get('spec').get('containers'))
        qos_count = 0
        mem_request = mem_request_bytes = mem_limit = mem_limit_bytes = 0
        cpu_request = cpu_limit = 0
        for container in dp.get('spec').get('template').get('spec').get('containers'):
            resource = container.get('resources')
            mem_request = mem_limit = mem_request_bytes = mem_limit_bytes = 0
            resource_request = resource.get('requests')
            if resource_request:
                mem_request = resource_request.get('memory') or 0
                mem_request_bytes = unit_trans_memory(mem_request)
                cpu_request = resource_request.get('cpu')
            resource_limit = resource.get('limits')
            if resource_limit:
                mem_limit = resource_limit.get('memory') or 0
                mem_limit_bytes = unit_trans_memory(mem_limit)
                cpu_limit = resource_limit.get('cpu')
            if mem_request == mem_limit != 0 and cpu_request == cpu_limit != 0:
                qos_count += 1
            if replicas != 0:
                count += 1
                sum_mem_request_bytes += mem_request_bytes * replicas
                sum_cpu_request_float += unit_trans_cpu(cpu_request) * replicas
                sum_mem_limit_bytes += mem_limit_bytes * replicas
                sum_cpu_limit_float += unit_trans_cpu(cpu_limit) * replicas
        qos_ratio = "%s/%s" % (qos_count, container_count)
        table_data.append(
            [namespace, name, replicas, container_count, qos_ratio, cpu_request, cpu_limit, mem_request, mem_limit, generation])
    sum_mem_request = int(sum_mem_request_bytes / 1024 / 1024) + 1
    sum_mem_limit = int(sum_mem_limit_bytes / 1024 / 1024) + 1
    print(tabulate(tabular_data=table_data,
                   headers=['namespace', f'{kind}名称', 'replicas', '容器数量', 'Guaranteed容器比例', 'CPU请求', 'CPU上限', 'MEM请求', 'MEM上限',
                            '迭代次数'],
                   tablefmt=args.fmt, showindex=True)
          )
    print(tabulate(
        tabular_data=[[sum_cpu_request_float, sum_cpu_limit_float, sum_mem_request, sum_mem_limit]],
        headers=['CPU请求之和(个)', 'CPU上限之和(个)', 'MEM请求之和(G)', 'MEM上限之和(G)'],
        tablefmt=args.fmt, showindex=False)
    )


def main():
    print_dp_memory()
