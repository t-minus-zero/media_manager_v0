
def key_event_js():
        script = """

document.addEventListener('keydown', function(event) {
    const key = event.key; // Get the key pressed

    if (key === "ArrowRight" || key === "ArrowLeft") {
        // Handle ArrowRight and ArrowLeft keys
        htmx.ajax(
            'POST',
            '/key-arrow-left-right',
            {
                values: { key: key },
                target: '#screen-container',
                swap: 'beforeend'
            }
        );
    } else {
        // Handle all other keys by setting hx-vals and triggering a custom HTMX event
        const dynamicElement = document.getElementById('dynamic-element');
        
        if (dynamicElement) {
            // Set the key value dynamically in the hx-vals attribute
            dynamicElement.setAttribute('hx-vals', JSON.stringify({ key: key }));
            
            // Trigger the custom HTMX event
            htmx.trigger(dynamicElement, 'customTrigger');
        }
    }
});

        """
        return script