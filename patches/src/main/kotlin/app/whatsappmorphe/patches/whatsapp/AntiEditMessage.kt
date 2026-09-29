package app.whatsappmorphe.patches.whatsapp

import app.morphe.patcher.Fingerprint
import app.morphe.patcher.extensions.InstructionExtensions.addInstructions
import app.morphe.patcher.patch.bytecodePatch
import app.morphe.patcher.string
import app.whatsappmorphe.patches.shared.Constants.WHATSAPP

@Suppress("unused")
val antiEditMessage = bytecodePatch(
    name = "Anti Edit",
    description = "Keep the original local message state when the known edit-info path is present.",
    default = false
) {
    compatibleWith(WHATSAPP)

    execute {
        val fingerprint = Fingerprint(
            returnType = "V",
            filters = listOf(string("MessageEditInfoStore/insertEditInfo/missing information in the FMessage"))
        )
        val method = fingerprint.methodOrNull ?: return@execute
        method.addInstructions(0, "return-void")
    }
}
