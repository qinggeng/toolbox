import subprocess
import json

def enum_windows():
    script = '''
Add-Type @"
    using System;
    using System.Runtime.InteropServices;

    public class Win32 {
        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);

        public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpWindowText, int nMaxCount);

        [DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        public static extern int GetWindowTextLength(IntPtr hWnd);

        [DllImport("user32.dll", SetLastError = true)]
        public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
    }
"@

$windows = @()

$enumWindowsProc = [Win32]::EnumWindows([Win32]::EnumWindowsProc {
    param($hWnd, $lParam)

    $textLength = [Win32]::GetWindowTextLength($hWnd)
    if ($textLength -gt 0) {
        $windowText = New-Object System.Text.StringBuilder ($textLength + 1)
        [Win32]::GetWindowText($hWnd, $windowText, $windowText.Capacity)
        $processId = [uint32]::MaxValue
        [Win32]::GetWindowThreadProcessId($hWnd, [ref]$processId) | Out-Null

        $windows += @{
            Handle = $hWnd
            Text = $windowText.ToString()
            ProcessId = $processId
        }
    }

    $true
}

[Win32]::EnumWindows($enumWindowsProc, [IntPtr]::Zero) | Out-Null

$windows | ConvertTo-Json
    '''.strip()

    result = subprocess.run(['powershell', '-Command', script], capture_output=True, text=True)
    print(result.stderr)
    windows = json.loads(result.stdout)

    return windows
