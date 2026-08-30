from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from .models import (
    Banknote,
    NoteDisposition,
    ProcessedNote,
    ProcessingMode,
    ProcessingSummary,
)
from .profiles import DeviceProfile


class CashProcessor:
    """Original cash-processing simulation engine.

    The engine models generic banknote-processing decisions for portfolio and
    training use. It does not emulate proprietary G+D firmware or protocols.
    """

    def __init__(self, profile: DeviceProfile, supported_currencies: set[str] | None = None):
        self.profile = profile
        self.supported_currencies = supported_currencies or {"TRY", "EUR", "USD"}

    def process(
        self,
        notes: Iterable[Banknote],
        mode: ProcessingMode = ProcessingMode.DENOMINATION,
    ) -> tuple[list[ProcessedNote], ProcessingSummary]:
        processed: list[ProcessedNote] = []
        summary = ProcessingSummary(device_profile=self.profile.key, mode=mode)
        output_load = defaultdict(int)

        for note in notes:
            summary.input_count += 1
            result = self._decide(note, mode, output_load)
            processed.append(result)
            output_load[result.output] += 1
            summary.outputs[result.output] = summary.outputs.get(result.output, 0) + 1

            if result.disposition == NoteDisposition.ACCEPTED:
                summary.accepted_count += 1
                summary.accepted_value += note.denomination
                summary.denomination_counts[note.denomination] = (
                    summary.denomination_counts.get(note.denomination, 0) + 1
                )
                if mode == ProcessingMode.SERIAL_CAPTURE and self.profile.serial_number_reading:
                    summary.serials.append(note.serial_number)
            else:
                summary.rejected_count += 1
                reason = result.reason or result.disposition.value
                summary.rejects_by_reason[reason] = summary.rejects_by_reason.get(reason, 0) + 1

        return processed, summary

    def _decide(
        self,
        note: Banknote,
        mode: ProcessingMode,
        output_load: dict[str, int],
    ) -> ProcessedNote:
        if note.currency not in self.supported_currencies:
            return ProcessedNote(
                note=note,
                disposition=NoteDisposition.REJECTED_UNSUPPORTED,
                output="reject",
                reason="unsupported_currency",
            )

        if not note.authentic:
            return ProcessedNote(
                note=note,
                disposition=NoteDisposition.REJECTED_AUTH,
                output="reject",
                reason="authentication_reject",
            )

        if mode == ProcessingMode.FITNESS and self.profile.fitness_sorting and not note.fit:
            return ProcessedNote(
                note=note,
                disposition=NoteDisposition.REJECTED_FITNESS,
                output="reject",
                reason="unfit_note",
            )

        output = self._select_output(note, mode, output_load)
        return ProcessedNote(
            note=note,
            disposition=NoteDisposition.ACCEPTED,
            output=output,
        )

    def _select_output(
        self,
        note: Banknote,
        mode: ProcessingMode,
        output_load: dict[str, int],
    ) -> str:
        stacker_count = max(1, self.profile.output_stackers)

        if mode == ProcessingMode.DENOMINATION:
            index = abs(hash((note.currency, note.denomination))) % stacker_count
            return f"stacker-{index + 1}"

        if mode == ProcessingMode.ORIENTATION:
            index = abs(hash(note.orientation)) % stacker_count
            return f"stacker-{index + 1}"

        # Count, fitness and serial-capture modes distribute accepted notes
        # toward the currently least-loaded stacker.
        candidates = [f"stacker-{i}" for i in range(1, stacker_count + 1)]
        return min(candidates, key=lambda name: output_load.get(name, 0))
