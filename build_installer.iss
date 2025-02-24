; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Volume Labeler"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Valer"
#define MyAppURL "https://github.com/Valer100/Volume-Labeler"
#define MyAppExeName "volume_labeler.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{51F6F747-0927-4042-A056-F7D5BBA6E81A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableDirPage=yes
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
DisableWelcomePage=no
LicenseFile=LICENSE
PrivilegesRequired=lowest
OutputDir=build
OutputBaseFilename=volume_labeler_installer_x64
SetupIconFile=assets/installer/icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
MinVersion=10.0
UninstallDisplayName=Volume Labeler
UninstallDisplayIcon={app}\{#MyAppExeName}
WizardSmallImageFile=assets\installer\icon.bmp
WizardImageFile=assets\installer\banner.bmp
WizardSizePercent=100
VersionInfoVersion=1.0.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "contextmenuintegration"; Description: "Show in the volumes' context menu"; GroupDescription: "Other options:"

[Files]
Source: "build\volume_labeler\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "build\volume_labeler\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "Change the label and the icon of a volume easily."
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "Change the label and the icon of a volume easily."; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\Classes\Drive\shell\Volume Labeler"; ValueType: string; ValueName: ""; ValueData: "Customize with Volume Labeler"; Flags: uninsdeletekey; Tasks: contextmenuintegration
Root: HKCU; Subkey: "Software\Classes\Drive\shell\Volume Labeler"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\volume_labeler.exe,0"; Flags: uninsdeletekey; Tasks: contextmenuintegration
Root: HKCU; Subkey: "Software\Classes\Drive\shell\Volume Labeler\command"; ValueType: string; ValueName: ""; ValueData: """{app}\volume_labeler.exe"" --volume %1"; Flags: uninsdeletekey; Tasks: contextmenuintegration

[UninstallDelete]
Type: filesandordirs; Name: "{userappdata}\Volume Labeler"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard();
begin
  WizardForm.WelcomeLabel1.Font.Name := 'Segoe UI Bold';
  WizardForm.WelcomeLabel1.Font.Size := 15;
  WizardForm.WelcomeLabel2.Top := WizardForm.WelcomeLabel2.Top + 20;
  
  WizardForm.FinishedHeadingLabel.Font.Name := 'Segoe UI Bold';
  WizardForm.FinishedHeadingLabel.Font.Size := 15;
  WizardForm.FinishedLabel.Top := WizardForm.FinishedLabel.Top + 20;
end;