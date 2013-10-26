 $("#treeview-left").kendoTreeView({
    dragAndDrop: true,
    dataSource: [
        { text: "Furniture", expanded: true, items: [
            { text: "Tables & Chairs" },
            { text: "Sofas" },
            { text: "Occasional Furniture" }
        ] },
        { text: "Decor", items: [
            { text: "Bed Linen" },
            { text: "Curtains & Blinds" },
            { text: "Carpets" }
        ] }
    ]
});