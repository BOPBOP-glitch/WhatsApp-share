package app.whatsappmorphe.patches.whatsapp

import app.morphe.patcher.Fingerprint
import app.morphe.patcher.extensions.InstructionExtensions.addInstructions
import app.morphe.patcher.patch.bytecodePatch
import app.morphe.patcher.string
import app.whatsappmorphe.patches.shared.Constants.WHATSAPP

@Suppress("unused")
val antiDisappearing = bytecodePatch(
    name = "Anti Disappearing",
    description = "Keep disappearing messages available locally when the known expiry path is present.",
    default = false
) {
    compatibleWith(WHATSAPP)

    execute {
        val fingerprint = Fingerprint(
            returnType = "V",
            filters = listOf(string("expire_timestamp"))
        )
        val method = fingerprint.methodOrNull ?: return@execute
        method.addInstructions(0, "return-void")
    }
}
