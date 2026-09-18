import re
out = """
        <div class="flex items-center justify-between p-space-md rounded-DEFAULT hover:bg-surface-container-low transition-colors" style="padding:16px; border-radius:16px; transition:0.2s;">
            <div class="flex items-center gap-space-md min-w-0" style="gap:16px;">
"""
print(repr(re.sub(r'^[ \t]+', '', out, flags=re.MULTILINE)))
