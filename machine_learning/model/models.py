#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List


@dataclass
class Sample:
    label: str
    data: List[float]


@dataclass
class SampleGroup:
    label: str
    samples: List[Sample]


def to_sample(label: str, data: List[float]) -> Sample:
    return Sample(label=label, data=data)


def to_sample_group(label: str, samples: List[List[float]]) -> SampleGroup:
    samples = [
        Sample(label=label, data=data) for data in samples
    ]
    return SampleGroup(label=label, samples=samples)
