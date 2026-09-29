package app.whatsappmorphe.patches.whatsapp

import app.morphe.patcher.Fingerprint
import app.morphe.patcher.extensions.InstructionExtensions.addInstructions
import app.morphe.patcher.patch.bytecodePatch
import app.morphe.patcher.string
import app.whatsappmorphe.patches.shared.Constants.WHATSAPP

@Suppress("unused")
val enableCopyStatus = bytecodePatch(
    name = "Copy Statuses",
    description = "Enable the known local copy-status path when available.",
    default = false
) {
    compatibleWith(WHATSAPP)

    execute {
        val fingerprint = Fingerprint(
            returnType = "V",
            filters = listOf(string("conversation/copymessage/npe"))
        )
        val method = fingerprint.methodOrNull ?: return@execute
        method.addInstructions(0, "return-void")
    }
}
