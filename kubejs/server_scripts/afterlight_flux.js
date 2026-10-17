// Island Flux Dust uses ordinary Obsidian and preserves native Bedrock and Flux Block recipes.
BlockEvents.leftClicked('minecraft:obsidian', event => {
  var top = event.block;
  if (top.level.isClientSide() || !event.item.isEmpty() || event.player.isFake()) return;
  var gap = top.down;
  if (String(gap.id) !== 'minecraft:air' || String(gap.down.id) !== 'minecraft:obsidian') return;

  // Only Redstone inside the empty gap is consumed, with excess items left for the next batch.
  var remaining = 512;
  var consumed = 0;
  top.level.getEntitiesWithin(AABB.ofBlock(gap.pos)).forEach(entity => {
    if (remaining <= 0 || String(entity.type) !== 'minecraft:item') return;
    var stack = entity.item;
    if (String(stack.id) !== 'minecraft:redstone') return;
    var amount = Math.min(remaining, stack.getCount());
    var leftover = stack.copy();
    leftover.shrink(amount);
    if (leftover.isEmpty()) entity.discard();
    else entity.setItem(leftover);
    remaining -= amount;
    consumed += amount;
  });
  if (consumed === 0) return;

  // The upper block descends into the gap; the base remains reusable and output stacks stay valid.
  top.set('minecraft:air');
  gap.set('minecraft:obsidian');
  while (consumed > 0) {
    var count = Math.min(64, consumed);
    top.popItem(Item.of('fluxnetworks:flux_dust', count));
    consumed -= count;
  }
});
