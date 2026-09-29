package app.whatsappmorphe.patches.whatsapp

import app.morphe.patcher.Fingerprint
import app.morphe.patcher.extensions.InstructionExtensions.addInstructions
import app.morphe.patcher.patch.bytecodePatch
import app.morphe.patcher.string
import app.whatsappmorphe.patches.shared.Constants.WHATSAPP

@Suppress("unused")
val antiRevoke = bytecodePatch(
    name = "Anti Revoke",
    description = "Keep revoked messages and statuses available locally.",
    default = false
) {
    compatibleWith(WHATSAPP)

    execute {
        val fingerprint = Fingerprint(
            returnType = "V",
            filters = listOf(string("msgstore/revoke/missing-old-id "))
        )
        val method = fingerprint.methodOrNull ?: return@execute

        method.addInstructions(
            0,
            """
                return-void
            """.trimIndent()
        )
    }
}
