#!/usr/bin/env python3
"""Convert SharePoint metadata.json records to compact markdown.

The workspace contains three record families:
- Concession Request System
- NCR Log System
- Fault System

Each converter keeps identifiers, part/status context, people, and narrative
fields that are useful for search/vectorization, while dropping SharePoint API
noise, numeric lookup ids, GUIDs, and empty fields.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable


TYPE_BY_SP_NAME = {
    "concession_x0020_request_x0020_system": "concession",
    "ncr_x0020_log_x0020_system": "ncr",
    "fault_x0020_system": "fault",
}

TYPE_BY_DIR = {
    "Concession Request System": "concession",
    "NCR Log System": "ncr",
    "Fault System": "fault",
}

SYSTEM_TITLE = {
    "concession": "Concession Request",
    "ncr": "NCR",
    "fault": "Fault",
}

FIELD_LABELS = {
    "Acceptance_x0020_Date": "Acceptance date",
    "Actions_x0020_For_x0020_Factory": "Factory actions",
    "AffectedCarArea": "Affected area",
    "Assembly_x0020_Number": "Assembly number",
    "Assigned_x0020_To": "Assigned to",
    "Batch_x0020_Quantity": "Batch quantity",
    "BusinessUnitsAffected": "Business units",
    "CarArea": "Car area",
    "Chassis": "Chassis",
    "CI_x0020_Action_x0020_No_x002e_": "CI action",
    "Company": "Company",
    "Completion_x0020_Date": "Completion date",
    "Component_x0020_Class": "Class",
    "Component_x0020_Class_Right": "Class right",
    "Concession_x0020_Closed": "Closed",
    "Concession_x0020_Type": "Type",
    "Containment_x0020_Action": "Containment",
    "Corrective_x0020_Action": "Corrective action",
    "Date_x0020_Raised": "Raised",
    "Delivery_x0020_Due_x0020_Date": "Due",
    "Description_x0020_of_x0020_Part": "Part description",
    "Description_x0020_Of_x0020_Part_": "Part description right",
    "Disposition_x0020_Comments": "Disposition comments",
    "Disposition_x0020_Date": "Disposition date",
    "Disposition_x0020_Decision": "Disposition",
    "Dispositioner": "Dispositioner",
    "Documentation": "Documentation",
    "Drawing_x0020_Error_x0020_Type": "Drawing error",
    "Drawing_x0020_Revision": "Drawing rev",
    "Drawing_x0020_Revision_Right": "Drawing rev right",
    "DVP_x0020_Component": "DVP component",
    "DMRCode": "DMR code",
    "Electronics_x0020_Affected": "Electronics affected",
    "Event1": "Event",
    "Factory_x0020_Comments": "Factory comments",
    "Factory_x0020_Investigations_x00": "Factory investigation",
    "Fault_x0020_Status": "Status",
    "GRN_x0020_No_x002e_": "GRN",
    "HiddenAttachments": "Hidden attachments",
    "Impact": "Impact",
    "Impact_x0020_Supplier": "Supplier impact",
    "ImpactSupplier": "Supplier impact",
    "Impacts_x0020_Aero": "Aero impact",
    "Impacts_x0020_Legality": "Legality impact",
    "Inspection_x0020_Process": "Inspection process",
    "Inspection_x0020_Type": "Inspection type",
    "InvestigationRequired": "Investigation required",
    "Issue_x0020_Conjecture": "Conjecture",
    "Issue_x0020_Department": "Department",
    "Issue_x0020_Detailed_x0020_Descr": "Description",
    "Issue_x0020_ID": "Issue",
    "Issue_x0020_Priority": "Priority",
    "Issue_x0020_Type": "Type",
    "Job_x0020_Card_x0020_No": "Job card",
    "Job_x0020_No_x002e_": "Job",
    "Job_x0020_Number": "Job",
    "Lot_x0020_Life_x0020_No_x002e_": "Lot/life",
    "MeetingNotes": "Meeting notes",
    "Mobile": "Mobile",
    "NCR_x0020_Cause_x0020_Department": "Cause department",
    "NCR_x0020_Status": "Status",
    "NCRNumber": "NCR",
    "NCRSeverity": "Severity",
    "Non_x0020_Conformance": "Non-conformance",
    "Part_x0020_Description": "Part description",
    "Part_x0020_Mileage": "Part mileage",
    "Part_x0020_No_Right": "Part no right",
    "Part_x0020_No_x002e_": "Part no",
    "Part_x0020_Number": "Part no",
    "Project_x0020_No_x002e_": "Project",
    "ProjectNumbers": "Projects",
    "Purchase_x0020_Order_x0020_Numbe": "PO",
    "Purchase_x0020_Order_x0020_Numbe0": "PO right",
    "Quantity_x0020_Affected": "Qty",
    "Quantity_x0020_Affected_Other": "Qty right",
    "RBT_x0020_Buyer_x0020_Name": "Buyer",
    "Raised_x0020_By": "Raised by",
    "Redbull_x0020_Acceptance_x0020_N": "Red Bull acceptance",
    "Reported_x0020_By": "Reported by",
    "Repeat_x0020_Fault": "Repeat",
    "Resolution_x0020_Workarounds_x00": "Resolution/workarounds",
    "Responsible_x0020_Designer": "Designer",
    "Responsible_x0020_Person_x005C_B": "Responsible person",
    "Responsible_x0020_RBT_x0020_Desi": "Designer",
    "Root_x0020_Cause": "Root cause",
    "Root_x0020_Cause_x0020_and_x0020": "Root cause status",
    "Root_x0020_Cause_x0020_Ownership": "Root cause ownership",
    "Serial_x0020_No_x002e_": "Serial no",
    "Session": "Session",
    "SQE": "SQE",
    "Supplier_x0020_Contact": "Supplier contact",
    "Supplier_x0020_Details": "Supplier",
    "Supplier_x0020_Job_x0020_Number": "Supplier job",
    "Supplier_x005C_Internal_x0020_De": "Supplier/internal dept",
    "TrackedPartTLS": "TLS tracked part",
    "Transponder_x0020_Number": "Transponder",
}

FIELD_ORDER = {
    "concession": [
        "Date_x0020_Raised",
        "Concession_x0020_Closed",
        "Concession_x0020_Type",
        "Disposition_x0020_Decision",
        "Disposition_x0020_Date",
        "Dispositioner",
        "Supplier_x0020_Details",
        "Supplier_x0020_Contact",
        "RBT_x0020_Buyer_x0020_Name",
        "Responsible_x0020_RBT_x0020_Desi",
        "SQE",
        "Part_x0020_No_x002e_",
        "Description_x0020_of_x0020_Part",
        "Drawing_x0020_Revision",
        "Component_x0020_Class",
        "Part_x0020_No_Right",
        "Description_x0020_Of_x0020_Part_",
        "Drawing_x0020_Revision_Right",
        "Component_x0020_Class_Right",
        "Quantity_x0020_Affected",
        "Quantity_x0020_Affected_Other",
        "Purchase_x0020_Order_x0020_Numbe",
        "Supplier_x0020_Job_x0020_Number",
        "Delivery_x0020_Due_x0020_Date",
        "Documentation",
        "Inspection_x0020_Type",
        "ImpactSupplier",
        "InvestigationRequired",
        "Root_x0020_Cause_x0020_and_x0020",
        "Non_x0020_Conformance",
        "Disposition_x0020_Comments",
        "Containment_x0020_Action",
        "Corrective_x0020_Action",
        "Root_x0020_Cause",
    ],
    "ncr": [
        "Date_x0020_Raised",
        "NCR_x0020_Status",
        "Disposition_x0020_Decision",
        "Disposition_x0020_Date",
        "Dispositioner",
        "NCRSeverity",
        "DMRCode",
        "Supplier_x005C_Internal_x0020_De",
        "Raised_x0020_By",
        "Responsible_x0020_Designer",
        "Responsible_x0020_Person_x005C_B",
        "SQE",
        "Part_x0020_No_x002e_",
        "Description_x0020_of_x0020_Part",
        "Drawing_x0020_Revision",
        "Component_x0020_Class",
        "Quantity_x0020_Affected",
        "Batch_x0020_Quantity",
        "Job_x0020_No_x002e_",
        "Project_x0020_No_x002e_",
        "Purchase_x0020_Order_x0020_Numbe",
        "Inspection_x0020_Process",
        "Impact_x0020_Supplier",
        "Impacts_x0020_Aero",
        "Impacts_x0020_Legality",
        "InvestigationRequired",
        "Root_x0020_Cause_x0020_Ownership",
        "Redbull_x0020_Acceptance_x0020_N",
        "Non_x0020_Conformance",
        "Disposition_x0020_Comments",
        "Root_x0020_Cause",
        "Containment_x0020_Action",
        "Corrective_x0020_Action",
        "MeetingNotes",
    ],
    "fault": [
        "Issue_x0020_ID",
        "Fault_x0020_Status",
        "Issue_x0020_Type",
        "Issue_x0020_Priority",
        "Reported_x0020_By",
        "Assigned_x0020_To",
        "Chassis",
        "CarArea",
        "AffectedCarArea",
        "BusinessUnitsAffected",
        "Event1",
        "Session",
        "Part_x0020_Number",
        "Part_x0020_Description",
        "Part_x0020_Mileage",
        "Lot_x0020_Life_x0020_No_x002e_",
        "Assembly_x0020_Number",
        "Transponder_x0020_Number",
        "ProjectNumbers",
        "Electronics_x0020_Affected",
        "Repeat_x0020_Fault",
        "Impact",
        "Issue_x0020_Department",
        "Issue_x0020_Detailed_x0020_Descr",
        "Issue_x0020_Conjecture",
        "Factory_x0020_Comments",
        "Factory_x0020_Investigations_x00",
        "Actions_x0020_For_x0020_Factory",
        "Resolution_x0020_Workarounds_x00",
        "HiddenAttachments",
    ],
}


class TextExtractor(HTMLParser):
    """Small HTML-to-text extractor for SharePoint rich text fields."""

    BLOCK_TAGS = {"p", "div", "li", "tr", "table", "ul", "ol"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "br":
            self.parts.append("\n")
        elif tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def handle_entityref(self, name: str) -> None:
        self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.parts.append(f"&#{name};")

    def text(self) -> str:
        return "".join(self.parts)


def clean_text(value: Any) -> str:
    text = str(value)
    text = text.replace("\u200b", "")
    if "<" in text and ">" in text:
        parser = TextExtractor()
        parser.feed(text)
        text = parser.text()
    text = html.unescape(html.unescape(text))
    text = text.replace("\r", "\n").replace("\xa0", " ")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def value_to_text(value: Any) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return ", ".join(filter(None, (value_to_text(item) for item in value)))
    if isinstance(value, dict):
        if "__deferred" in value:
            return ""
        if "Title" in value:
            return clean_text(value["Title"])
        if "results" in value:
            return value_to_text(value["results"])
        return ""
    return clean_text(value)


def detect_type(data: dict[str, Any], source: Path | None = None) -> str:
    sp_type = (
        data.get("Fields", {})
        .get("__metadata", {})
        .get("type", "")
        .lower()
    )
    for marker, record_type in TYPE_BY_SP_NAME.items():
        if marker in sp_type:
            return record_type

    if source:
        for part in source.parts:
            if part in TYPE_BY_DIR:
                return TYPE_BY_DIR[part]

    raise ValueError("Unable to detect metadata type")


def first_text(fields: dict[str, Any], keys: Iterable[str]) -> str:
    for key in keys:
        value = value_to_text(fields.get(key))
        if value:
            return value
    return ""


def add_line(lines: list[str], label: str, value: str) -> None:
    if not value:
        return
    if "\n" in value:
        lines.append(f"{label}:\n{value}")
    else:
        lines.append(f"{label}: {value}")


def metadata_to_markdown(data: dict[str, Any], source: Path | None = None) -> str:
    record_type = detect_type(data, source)
    fields = data.get("Fields", {})
    title = value_to_text(data.get("Title"))

    if record_type == "concession":
        identifier = title or f"CR{data.get('Id')}"
    elif record_type == "fault":
        identifier = first_text(fields, ["Issue_x0020_ID"]) or f"RBR{data.get('Id')}"
    else:
        identifier = title or str(data.get("Id"))

    part = first_text(
        fields,
        [
            "Part_x0020_No_x002e_",
            "Part_x0020_Number",
            "Part_x0020_No_Right",
        ],
    )
    description = first_text(
        fields,
        [
            "Description_x0020_of_x0020_Part",
            "Part_x0020_Description",
            "Description_x0020_Of_x0020_Part_",
        ],
    )

    heading_bits = [SYSTEM_TITLE[record_type], identifier]
    if record_type == "fault" and title and title != identifier:
        heading_bits.append(title)
    elif part:
        heading_bits.append(part)
    elif description:
        heading_bits.append(description)

    lines = ["# " + " - ".join(str(bit) for bit in heading_bits if bit)]
    add_line(lines, "Record id", value_to_text(data.get("Id")))
    if data.get("Created"):
        add_line(lines, "Created", clean_text(data["Created"]))
    if data.get("Modified"):
        add_line(lines, "Modified", clean_text(data["Modified"]))

    for key in FIELD_ORDER[record_type]:
        label = FIELD_LABELS.get(key, readable_label(key))
        add_line(lines, label, value_to_text(fields.get(key)))

    attachments = data.get("Attachments") or []
    if isinstance(attachments, list) and attachments:
        names = []
        for item in attachments:
            if isinstance(item, dict):
                names.append(
                    value_to_text(
                        item.get("FileName")
                        or item.get("Name")
                        or item.get("ServerRelativeUrl")
                    )
                )
            else:
                names.append(value_to_text(item))
        add_line(lines, "Attachments", ", ".join(filter(None, names)))
    elif value_to_text(fields.get("Attachments")) == "yes":
        add_line(lines, "Attachments", "yes")

    return "\n".join(lines).strip() + "\n"


def readable_label(key: str) -> str:
    label = key.replace("_x0020_", " ")
    label = label.replace("_x002e_", ".")
    label = label.replace("_x005C_", "/")
    label = re.sub(r"_x[0-9A-Fa-f]{4}_", " ", label)
    label = label.replace("_", " ")
    label = re.sub(r"\s+", " ", label).strip()
    return label[:1].upper() + label[1:]


def convert_file(source: Path, output: Path | None = None) -> Path:
    with source.open(encoding="utf-8") as f:
        data = json.load(f)
    text = metadata_to_markdown(data, source)
    target = output or source.with_suffix(".md")
    target.write_text(text, encoding="utf-8")
    return target


def parse_metadata_file(source: str | Path) -> str:
    """Return compact markdown for one downloaded metadata.json file."""
    source_path = Path(source)
    with source_path.open(encoding="utf-8") as f:
        data = json.load(f)
    return metadata_to_markdown(data, source_path)


def convertMetadata(value: dict[str, Any]) -> None:
    """Handle an OCI object event by converting metadata.json to markdown."""
    import oci

    from file_convert import download_file, get_metadata_from_resource_id
    import rag_storage
    from shared import (
        UNIQUE_ID,
        getLogDir,
        log,
        shared_config,
        shared_signer,
    )

    log("<convertMetadata>")
    eventType = value["eventType"]
    namespace = value["data"]["additionalDetails"]["namespace"]
    bucketName = value["data"]["additionalDetails"]["bucketName"]
    resourceName = value["data"]["resourceName"]
    resourceId = value["data"]["resourceId"]
    resourceGenAI = resourceName + ".md"

    oci.object_storage.ObjectStorageClient(
        config=shared_config,
        signer=shared_signer,
    )

    if eventType in [
        "com.oraclecloud.objectstorage.createobject",
        "com.oraclecloud.objectstorage.updateobject",
    ]:
        metadata = get_metadata_from_resource_id(resourceId)
        local_file = download_file(namespace, bucketName, resourceName)
        text = parse_metadata_file(local_file)

        dest_file = getLogDir() + "/" + UNIQUE_ID + ".md"
        with open(dest_file, "w", encoding="utf-8") as f_out:
            f_out.write(text)

        rag_storage.upload_file(
            value=value,
            object_name=resourceGenAI,
            file_path=dest_file,
            content_type="text/markdown",
            metadata=metadata,
        )
    elif eventType == "com.oraclecloud.objectstorage.deleteobject":
        rag_storage.delete_file(value=value, object_name=resourceGenAI)
    log("</convertMetadata>")


def iter_metadata(paths: Iterable[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_file():
            yield path
        elif path.is_dir():
            yield from sorted(path.glob("*/metadata.json"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert metadata.json files to compact markdown."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("Concession Request System"), Path("NCR Log System"), Path("Fault System")],
        help="metadata.json file(s) or source directories. Defaults to all three systems.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print converted markdown instead of writing metadata.md files.",
    )
    args = parser.parse_args()

    files = list(iter_metadata(args.paths))
    if not files:
        raise SystemExit("No metadata.json files found.")

    for source in files:
        with source.open(encoding="utf-8") as f:
            data = json.load(f)
        text = metadata_to_markdown(data, source)
        if args.stdout:
            print(f"<!-- {source} -->")
            print(text)
        else:
            target = source.with_suffix(".md")
            target.write_text(text, encoding="utf-8")
            print(target)


if __name__ == "__main__":
    main()
