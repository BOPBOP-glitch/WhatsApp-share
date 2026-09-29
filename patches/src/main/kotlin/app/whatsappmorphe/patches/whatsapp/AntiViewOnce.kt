package app.whatsappmorphe.patches.whatsapp

import app.morphe.patcher.Fingerprint
import app.morphe.patcher.extensions.InstructionExtensions.addInstructions
import app.morphe.patcher.patch.bytecodePatch
import app.morphe.patcher.string
import app.whatsappmorphe.patches.shared.Constants.WHATSAPP
import com.android.tools.smali.dexlib2.iface.instruction.FiveRegisterInstruction
import com.android.tools.smali.dexlib2.iface.instruction.ReferenceInstruction
import com.android.tools.smali.dexlib2.iface.reference.MethodReference

@Suppress("unused")
val antiViewOnce = bytecodePatch(
    name = "Anti View Once",
    description = "Keep view-once media locally reusable when the known WhatsApp database paths are present.",
    default = false
) {
    compatibleWith(WHATSAPP)

    execute {
        var viewOnceInterface: String? = null
        var stateMethodName: String? = null

        val readFingerprint = Fingerprint(
            filters = listOf(string("GET_VIEW_ONCE_STATE_BY_MESSAGE_ROW_ID_SQL"))
        )
        val readMethod = readFingerprint.methodOrNull
        val readOriginal = readFingerprint.originalMethodOrNull

        if (readMethod != null && readOriginal?.implementation != null) {
            val instructions = readOriginal.implementation!!.instructions.toList()
            val invoke = instructions.lastOrNull { instruction ->
                instruction.opcode.name == "invoke-interface" &&
                    instruction is ReferenceInstruction &&
                    instruction is FiveRegisterInstruction
            }

            if (invoke is ReferenceInstruction && invoke is FiveRegisterInstruction) {
                val ref = invoke.reference as? MethodReference
                if (ref != null) {
                    viewOnceInterface = ref.definingClass
                    stateMethodName = ref.name

                    val index = instructions.indexOf(invoke)
                    if (index >= 0) {
                        readMethod.addInstructions(index, "const/4 v${invoke.registerD}, 0x0")
                    }
                }
            }
        }

        val writeFingerprint = Fingerprint(
            filters = listOf(string("UPDATE_VIEW_ONCE_SQL"))
        )
        writeFingerprint.methodOrNull?.let { method ->
            if (method.parameters.isNotEmpty()) {
                method.addInstructions(0, "const/4 p1, 0x0")
            }
        }

        val iface = viewOnceInterface
        val methodName = stateMethodName
        if (iface != null && methodName != null) {
            classDefForEach { def ->
                if (!def.interfaces.contains(iface)) return@classDefForEach

                val original = def.methods.firstOrNull { method ->
                    method.name == methodName &&
                        method.parameters.isNotEmpty() &&
                        method.returnType == "V"
                } ?: return@classDefForEach

                val mutable = mutableClassDefBy(def).methods.firstOrNull { method ->
                    method.name == original.name &&
                        method.parameters == original.parameters &&
                        method.returnType == original.returnType
                } ?: return@classDefForEach

                mutable.addInstructions(0, "const/4 p1, 0x0")
            }
        }

        // V2 intentionally does not apply a global FLAG_SECURE bypass.
        // The previous implementation scanned every Window utility method and could affect
        // unrelated privacy-sensitive screens. Screenshot support will return only after
        // a WhatsApp-version-specific fingerprint is validated.
    }
}
