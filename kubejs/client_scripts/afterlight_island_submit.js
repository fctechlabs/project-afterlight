// Sky GUIs receives one creation request per screen submission, including keyboard activation.
const ALCreateScreen = Java.loadClass('de.melanx.skyguis.client.screen.CreateTeamScreen');
const ALButton = Java.loadClass('net.minecraft.client.gui.components.Button');
const ALEditBox = Java.loadClass('net.minecraft.client.gui.components.EditBox');
let alCreatePending = false;

// Only the translated Create button is intercepted; other controls retain their normal behavior.
function alIsCreateButton(widget) {
  return widget instanceof ALButton && String(widget.message.contents).indexOf('screen.skyguis.button.create') >= 0;
}

// Blank names retain the upstream random-name step without locking the screen.
function alSubmitIsland(event, button) {
  event.setCanceled(true);
  if (alCreatePending || !button.active) return;
  const children = event.screen.children();
  let hasName = false;
  children.forEach(widget => {
    if (widget instanceof ALEditBox && String(widget.value).trim().length > 0) hasName = true;
  });
  if (hasName) {
    alCreatePending = true;
    button.active = false;
  }
  button.onPress();
}

// Reinitializing the form after a failed request allows a corrected submission.
NativeEvents.onEvent('net.neoforged.neoforge.client.event.ScreenEvent$Init$Post', event => {
  if (event.screen instanceof ALCreateScreen) {
    alCreatePending = false;
  }
});

NativeEvents.onEvent('net.neoforged.neoforge.client.event.ScreenEvent$MouseButtonPressed$Pre', event => {
  if (!(event.screen instanceof ALCreateScreen) || event.button != 0) return;
  event.screen.children().forEach(widget => {
    if (alIsCreateButton(widget) && widget.isMouseOver(event.mouseX, event.mouseY)) alSubmitIsland(event, widget);
  });
});

NativeEvents.onEvent('net.neoforged.neoforge.client.event.ScreenEvent$KeyPressed$Pre', event => {
  if (!(event.screen instanceof ALCreateScreen) || [32, 257, 335].indexOf(event.keyCode) < 0) return;
  const focused = event.screen.focused;
  if (alIsCreateButton(focused)) alSubmitIsland(event, focused);
});
