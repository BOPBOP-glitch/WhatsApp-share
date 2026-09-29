package app.whatsappmorphe.patches.whatsapp

import app.morphe.patcher.Fingerprint
import app.morphe.patcher.extensions.InstructionExtensions.addInstructions
import app.morphe.patcher.patch.bytecodePatch
import app.morphe.patcher.string
import app.whatsappmorphe.patches.shared.Constants.WHATSAPP

@Suppress("unused")
val mediaQuality = bytecodePatch(
    name = "HD Media",
    description = "Prefer the highest media quality path supported by this WhatsApp build.",
    default = false
) {
    compatibleWith(WHATSAPP)

    execute {
        val fingerprint = Fingerprint(
            returnType = "Z",
            filters = listOf(string("ProcessVideoQuality(videoLimitMb="))
        )
        val method = fingerprint.methodOrNull ?: return@execute

        method.addInstructions(
            0,
            """
                const/4 v0, 0x1
                return v0
            """.trimIndent()
        )
    }
}
