document.addEventListener('DOMContentLoaded', () => {
    const addDocBtn = document.getElementById('add_doc_btn');
    const docsContainer = document.getElementById('docs_container');

    addDocBtn.addEventListener('click', () => {
        // Create container for new input + remove button
        const entryDiv = document.createElement('div');
        entryDiv.className = 'doc_entry';

        // Create new input
        const newInput = document.createElement('input');
        newInput.type = 'text';
        newInput.name = 'docs_link[]';
        newInput.placeholder = 'Current documents e.g. name|link';

        // Create remove button
        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.textContent = '×';
        removeBtn.className = 'remove_btn';
        removeBtn.addEventListener('click', () => {
            docsContainer.removeChild(entryDiv);
        });

        // Append input and remove button to the new entry
        entryDiv.appendChild(newInput);
        entryDiv.appendChild(removeBtn);

        docsContainer.appendChild(entryDiv);
    });
});
