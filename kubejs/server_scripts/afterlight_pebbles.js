// Starter gathering follows ATM10Sky's sneak interaction, dirt tag, and pebble probabilities.
var ALPebbleVariants = ['andesite', 'basalt', 'blackstone', 'diorite', 'granite', 'deepslate'];

// KubeJS supplies the server interaction and skips native events that protection already canceled.
BlockEvents.rightClicked(event => {
  if (String(event.hand) !== 'MAIN_HAND' || !event.item.isEmpty()) return;
  if (!event.player.isShiftKeyDown() || !event.block.hasTag('minecraft:dirt')) return;

  // Six of twelve equally likely outcomes give Stone; each other variant receives one outcome.
  var roll = Math.floor(Math.random() * 12);
  var material = roll < ALPebbleVariants.length ? ALPebbleVariants[roll] : 'stone';
  event.block.popItemFromFace(Item.of('exdeorum:' + material + '_pebble'), event.facing);
  event.player.swing();
});
