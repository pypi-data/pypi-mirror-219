#!/usr/bin/env python
"""Classes for reading multiple sequence alignment files in different formats."""


import re
import xml.dom.minidom

from cogent3.parse import (
    clustal,
    fasta,
    gbseq,
    gcg,
    genbank,
    nexus,
    paml,
    phylip,
    tinyseq,
)
from cogent3.parse.record import FileFormatError
from cogent3.util.io import get_format_suffixes, open_


_lc_to_wc = "".join([[chr(x), "?"]["A" <= chr(x) <= "Z"] for x in range(256)])
_compression = re.compile(r"\.(gz|bz2)$")


def FromFilenameParser(filename, format=None, **kw):
    """Arguments:
    - filename: name of the sequence alignment file
    - format: the multiple sequence file format
    """
    if format is None:
        format, _ = get_format_suffixes(filename)

    with open_(filename, newline=None, mode="rt") as f:
        data = f.read()

    return FromFileParser(data.splitlines(), format, **kw)


def FromFileParser(f, format, dialign_recode=False, **kw):
    format = format.lower()
    if format in XML_PARSERS:
        doctype = format
        format = "xml"
    else:
        doctype = None
    if format == "xml":
        source = dom = xml.dom.minidom.parse(f)
        if doctype is None:
            doctype = str(dom.doctype.name).lower()
        if doctype not in XML_PARSERS:
            raise FileFormatError(f"Unsupported XML doctype {doctype}")
        parser = XML_PARSERS[doctype]
    else:
        if format not in PARSERS:
            raise FileFormatError(f"Unsupported file format {format}")
        parser = PARSERS[format]
        source = f
    for name, seq in parser(source, **kw):
        if isinstance(seq, str):
            if dialign_recode:
                seq = seq.translate(_lc_to_wc)
            if not seq.isupper():
                seq = seq.upper()
        yield name, seq


def format_from_filename(filename, format=None):  # pragma: no cover
    from cogent3.util.warning import deprecated

    deprecated(
        "function",
        "cogent3.parse.sequence.format_from_filename",
        "cogent3.util.misc.get_format_suffixes",
        "2023.8",
    )
    """Detects format based on filename."""
    if format:
        return format
    else:
        r = _compression.search(filename)
        if r:
            filename = filename[: r.start()]

        return filename[filename.rfind(".") + 1 :]


PARSERS = {
    "phylip": phylip.MinimalPhylipParser,
    "paml": paml.PamlParser,
    "fasta": fasta.MinimalFastaParser,
    "mfa": fasta.MinimalFastaParser,
    "fa": fasta.MinimalFastaParser,
    "faa": fasta.MinimalFastaParser,
    "fna": fasta.MinimalFastaParser,
    "xmfa": fasta.MinimalXmfaParser,
    "gde": fasta.MinimalGdeParser,
    "aln": clustal.ClustalParser,
    "clustal": clustal.ClustalParser,
    "gb": genbank.RichGenbankParser,
    "gbk": genbank.RichGenbankParser,
    "gbff": genbank.RichGenbankParser,
    "genbank": genbank.RichGenbankParser,
    "msf": gcg.MsfParser,
    "nex": nexus.MinimalNexusAlignParser,
    "nxs": nexus.MinimalNexusAlignParser,
    "nexus": nexus.MinimalNexusAlignParser,
}

XML_PARSERS = {"gbseq": gbseq.GbSeqXmlParser, "tseq": tinyseq.TinyseqParser}
