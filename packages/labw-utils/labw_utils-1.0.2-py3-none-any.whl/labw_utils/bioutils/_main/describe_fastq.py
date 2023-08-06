"""
describe_fastq.py -- Lite Python-implemented fastqc.

SYNOPSIS: python -m labw_utils.bioutils describe_fastq [FASTQ] [[FASTQ]...]

where [FASTQ] are path to GTF files you wish to describe.
"""
import os

from labw_utils import UnmetDependenciesError
from labw_utils.typing_importer import List, Optional

try:
    import numpy as np
except ImportError:
    raise UnmetDependenciesError("numpy")

from labw_utils.bioutils.algorithm.sequence import get_gc_percent, decode_phred33
from labw_utils.bioutils.parser.fastq import FastqIterator
from labw_utils.commonutils.stdlib_helper.logger_helper import get_logger

_lh = get_logger(__name__)


def fastqc(filepath: str, outdir_path: Optional[str] = None):
    _lh.info("Start parsing '%s'...", filepath)
    if not os.path.exists(filepath):
        _lh.error("File '%s' not exist!", filepath)
    outdir_path = filepath + ".stats.d" if outdir_path is None else outdir_path
    os.makedirs(filepath + ".stats.d", exist_ok=True)
    with open(os.path.join(outdir_path, "all.tsv"), "wt") as all_writer:
        all_writer.write("\t".join((
            "SEQID",
            "GC",
            "LEN",
            "MEANQUAL"
        )) + "\n")
        max_read_length = 0
        for fastq_record in FastqIterator(filename=filepath):
            len_record = len(fastq_record)
            all_writer.write("\t".join((
                "\'" + fastq_record.seq_id + "\'",
                str(get_gc_percent(fastq_record.sequence)),
                str(len_record),
                str(np.mean(list(decode_phred33(fastq_record.quality))))
            )) + "\n")
            max_read_length = max(max_read_length, len_record)
    quality_sum = np.zeros(max_read_length, dtype=np.double)
    quality_cnt = np.zeros(max_read_length, dtype=np.double)
    for fastq_record in FastqIterator(filename=filepath):
        current_quality = np.array(list(decode_phred33(fastq_record.quality)))
        quality_sum[0:current_quality.shape[0]] += current_quality
        quality_cnt[0:current_quality.shape[0]] += 1
    quality = quality_sum / quality_cnt
    with open(os.path.join(outdir_path, "extension_stat.tsv"), "w") as extension_quality_writer:
        extension_quality_writer.write("\t".join(("POS", "QUAL")) + "\n")
        for pos, qual in enumerate(quality):
            extension_quality_writer.write("\t".join((
                str(pos),  # "POS",
                str(qual),  # "QUAL"
            )) + "\n")


def main(args: List[str]):
    for name in args:
        fastqc(name)
