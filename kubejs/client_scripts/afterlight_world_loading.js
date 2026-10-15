// Native world-loading labels remain live and centered below the approved artwork at every GUI scale.
const ALWorldMessageScreen = Java.loadClass('net.minecraft.client.gui.screens.GenericMessageScreen');
const ALWorldLevelScreen = Java.loadClass('net.minecraft.client.gui.screens.LevelLoadingScreen');
const ALWorldProgressScreen = Java.loadClass('net.minecraft.client.gui.screens.ProgressScreen');
const ALWorldReceivingScreen = Java.loadClass('net.minecraft.client.gui.screens.ReceivingLevelScreen');
const ALWorldConnectScreen = Java.loadClass('net.minecraft.client.gui.screens.ConnectScreen');
const ALWorldUniqueWidget = Java.loadClass('de.keksuccino.fancymenu.util.rendering.ui.widget.UniqueWidget');
const ALWorldButton = Java.loadClass('net.minecraft.client.gui.components.Button');

// FancyMenu's native TextWidget renderers use their original coordinates, so position those widgets directly after initialization.
function alPlaceWorldLoadingWidgets(screen) {
  if (!(screen instanceof ALWorldMessageScreen || screen instanceof ALWorldLevelScreen ||
      screen instanceof ALWorldProgressScreen || screen instanceof ALWorldReceivingScreen ||
      screen instanceof ALWorldConnectScreen)) return;
  const offsets = {message:40, percentage:39, header:53, stage:36, downloading_terrain:40, status:62};
  screen.children().forEach(widget => {
    const identifier = widget instanceof ALWorldUniqueWidget ? String(widget.getWidgetIdentifierFancyMenu()) : '';
    if (identifier === 'chunks' && screen instanceof ALWorldLevelScreen) {
      widget.visible = false;
    } else if (offsets[identifier] !== undefined) {
      widget.setX(Math.floor((screen.width - widget.getWidth()) / 2));
      widget.setY(screen.height - offsets[identifier]);
    } else if (screen instanceof ALWorldConnectScreen && widget instanceof ALWorldButton) {
      widget.setWidth(Math.floor(screen.width * 0.52));
      widget.setX(Math.floor(screen.width * 0.24));
      widget.setY(screen.height - 30);
    }
  });
}

NativeEvents.onEvent('net.neoforged.neoforge.client.event.ScreenEvent$Init$Post', event => {
  alPlaceWorldLoadingWidgets(event.screen);
});

// GenericMessageScreen arranges its message after initialization; restore the loading positions before it draws.
NativeEvents.onEvent('net.neoforged.neoforge.client.event.ScreenEvent$Render$Pre', event => {
  alPlaceWorldLoadingWidgets(event.screen);
});
