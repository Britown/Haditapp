import re

out = """
<div class="flex flex-col gap-space-xs">
""".replace("{count}", "2")

out += """
                        <div class="flex items-center justify-between p-space-md rounded-DEFAULT hover:bg-surface-container-low transition-colors" style="padding:16px; border-radius:16px; transition:0.2s;">
                            <div class="flex items-center gap-space-md min-w-0" style="gap:16px;">
                                <div class="w-10 h-10 rounded-DEFAULT bg-surface-container-low flex items-center justify-center text-on-surface-variant shrink-0" style="width:40px; height:40px; border-radius:12px; background:#f4f3f8; color:#4c4546;">
                                    <span class="material-symbols-outlined text-[20px]">{icon}</span>
                                </div>
"""

print("BEFORE:")
print(repr(out))

final = re.sub(r'^[ \t]+', '', out, flags=re.MULTILINE)
print("AFTER:")
print(repr(final))
