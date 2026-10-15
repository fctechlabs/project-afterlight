// The final cosmetic trophy is the sole Afterlight item; it supplies no earlier ingredient.
StartupEvents.registry('item', event => {
  event.create('afterlight:afterlight_beacon').displayName('Afterlight Beacon').texture('minecraft:item/nether_star').maxStackSize(1).tooltip('A world rebuilt, one craft at a time.');
});
