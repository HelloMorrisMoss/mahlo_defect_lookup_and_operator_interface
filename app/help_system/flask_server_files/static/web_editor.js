let currentArticlePath = null;
let currentArticleData = [];
let previousArticlePath = null;
let expandedFolders = new Set(["Root"]); // Root expanded by default
let previewedMediaPath = null;
let isSelectingInTree = false;
let selectionPurpose = ''; // 'BLOCK_MEDIA', 'BLOCK_LINK', 'CREATE_ARTICLE', 'MOVE_ARTICLE', 'MOVE_FOLDER'
let selectionBlockIndex = -1;
let selectionType = ''; // 'image', 'video', 'article', 'folder'
let selectionExtraData = null;
let checkedOutVersionId = null;

async function refreshArticleList() {
    const response = await fetch('api/structure');
    const tree = await response.json();
    const list = document.getElementById('article-list');
    list.innerHTML = '';

    // Sort children: folders first, then articles
    const sortedChildren = tree.children.sort((a, b) => {
        if (a.type !== b.type) return a.type === 'folder' ? -1 : 1;
        return a.name.localeCompare(b.name);
    });

    sortedChildren.forEach(child => {
        list.appendChild(renderTreeNode(child));
    });
}

function renderTreeNode(node) {
    const div = document.createElement('div');
    if (node.type === 'folder') {
        const isExpanded = expandedFolders.has(node.path) || node.name === "Root";
        const header = document.createElement('div');
        header.className = 'folder-item' + (node.is_media ? ' media-folder' : '');
        header.dataset.path = node.path;

        let label = node.name;
        if (node.is_media) {
            label += ` (${node.item_count || 0})`;
        }

        const toggleIcon = isExpanded ? '▼' : '▶';
        const folderIcon = node.is_media ? '📁' : (isExpanded ? '📂' : '📁');
        const editIcon = `<span class="folder-edit-icon" title="Folder Options">✏️</span>`;

        header.innerHTML = `<span class="article-icon" style="cursor:pointer; width: 10px; display: inline-block;">${toggleIcon}</span> <span class="article-icon">${folderIcon}</span> ${label}${editIcon}`;
        
        header.onclick = (e) => {
            e.stopPropagation();
            if (e.target.classList.contains('folder-edit-icon')) {
                showFolderOptions(node);
                return;
            }

            if (isSelectingInTree && selectionType === 'folder') {
                handleSelectionClick(node, header);
            }

            toggleFolder(node.path);
        };
        div.appendChild(header);

        const content = document.createElement('div');
        content.className = 'folder-content';
        content.style.display = isExpanded ? 'block' : 'none';

        const children = node.children || [];
        children.sort((a, b) => {
            if (a.type !== b.type) return a.type === 'folder' ? -1 : 1;
            return a.name.localeCompare(b.name);
        });

        children.forEach(child => {
            content.appendChild(renderTreeNode(child));
        });
        div.appendChild(content);
    } else {
        const item = document.createElement('div');
        item.className = 'article-item';
        item.dataset.path = node.path;
        if (node.path === currentArticlePath) item.classList.add('selected');
        if (node.path === previewedMediaPath) item.classList.add('media-selected');
        let icon = node.icon;
        if (!icon) {
            if (node.type === 'article') icon = 'ℹ️';
            else if (node.type === 'image') icon = '📷';
            else if (node.type === 'video') icon = '🎥';
            else icon = '📄';
        }
        item.innerHTML = `<span class="article-icon">${icon}</span> ${node.name}`;
        item.onclick = (e) => {
            e.stopPropagation();
            handleTreeItemClick(node, item);
        };
        div.appendChild(item);
    }
    return div;
}

function toggleFolder(path) {
    if (expandedFolders.has(path)) {
        expandedFolders.delete(path);
    } else {
        expandedFolders.add(path);
    }
    // We don't need to fetch from server just to toggle UI, but refreshArticleList does that.
    // For now, let's just re-render from local state if we had it, but refresh is safer.
    refreshArticleList();
}

function handleTreeItemClick(node, element) {
    if (isSelectingInTree) {
        handleSelectionClick(node, element);
        return;
    }

    if (node.type === 'article') {
        loadArticle(node.path, node.name);
    } else if (node.type === 'image' || node.type === 'video') {
        showMediaPreview(node);
    }
}

function showMediaPreview(node) {
    previewedMediaPath = node.path;

    // Update UI highlights
    document.querySelectorAll('.article-item').forEach(el => {
        el.classList.toggle('media-selected', el.dataset.path === node.path);
    });

    const container = document.getElementById('media-preview-container');
    const content = document.getElementById('media-preview-content');
    container.style.display = 'flex';

    const src = `media/${getDisplayPath(node.path)}`;
    if (node.type === 'image') {
        content.innerHTML = `<img src="${src}">`;
    } else if (node.type === 'video') {
        content.innerHTML = `<video src="${src}" controls autoplay></video>`;
    }
}

function closeMediaPreview() {
    previewedMediaPath = null;
    document.getElementById('media-preview-container').style.display = 'none';
    document.querySelectorAll('.article-item').forEach(el => {
        el.classList.remove('media-selected');
    });
}

function showMediaSelectorForBlock(blockIndex) {
    const block = currentArticleData[blockIndex];
    isSelectingInTree = true;
    selectionPurpose = 'BLOCK_MEDIA';
    selectionBlockIndex = blockIndex;
    selectionType = block.type; // 'image' or 'video'

    const popup = document.getElementById('selection-popup');
    const title = document.getElementById('selection-popup-title');
    const msg = document.getElementById('selection-popup-message');
    const error = document.getElementById('selection-error');
    const pathDisplay = document.getElementById('selection-path-display');
    const okBtn = document.getElementById('selection-ok-btn');

    title.textContent = `Select ${selectionType.charAt(0).toUpperCase() + selectionType.slice(1)}`;
    msg.textContent = `Please click an ${selectionType} in the tree navigation.`;
    error.style.display = 'none';
    pathDisplay.textContent = 'No file selected';
    okBtn.style.display = 'none';
    popup.style.display = 'block';
}

function showLinkSelectorForBlock(blockIndex) {
    isSelectingInTree = true;
    selectionPurpose = 'BLOCK_LINK';
    selectionBlockIndex = blockIndex;
    selectionType = 'article';

    const popup = document.getElementById('selection-popup');
    const title = document.getElementById('selection-popup-title');
    const msg = document.getElementById('selection-popup-message');
    const error = document.getElementById('selection-error');
    const pathDisplay = document.getElementById('selection-path-display');
    const okBtn = document.getElementById('selection-ok-btn');

    title.textContent = 'Select Target Article';
    msg.textContent = 'Please click an article in the tree navigation.';
    error.style.display = 'none';
    pathDisplay.textContent = 'No article selected';
    okBtn.style.display = 'none';
    popup.style.display = 'block';
}

function handleSelectionClick(node, element) {
    const error = document.getElementById('selection-error');
    const pathDisplay = document.getElementById('selection-path-display');
    const okBtn = document.getElementById('selection-ok-btn');

    if (node.type !== selectionType) {
        error.textContent = `Must be a ${selectionType}. Selected: ${node.type}`;
        error.style.display = 'block';
        pathDisplay.textContent = 'Invalid selection';
        okBtn.style.display = 'none';
        return;
    }

    // Validation for MOVE_FOLDER: cannot move into self or child
    if (selectionPurpose === 'MOVE_FOLDER') {
        const sourcePath = selectionExtraData;
        if (node.path === sourcePath || node.path.startsWith(sourcePath + '/')) {
            error.textContent = "Cannot move a folder into itself or its subfolders.";
            error.style.display = 'block';
            pathDisplay.textContent = 'Invalid selection';
            okBtn.style.display = 'none';
            return;
        }
    }

    error.style.display = 'none';
    pathDisplay.textContent = getDisplayPath(node.path);
    okBtn.style.display = 'inline-block';
    okBtn.onclick = () => confirmSelection(node.path);

    // Also show preview while selecting if it's media
    if (node.type === 'image' || node.type === 'video') {
        showMediaPreview(node);
    }
}

function confirmSelection(path) {
    if (selectionPurpose === 'BLOCK_LINK') {
        currentArticleData[selectionBlockIndex].target = getDisplayPath(path);
        renderEditor();
        renderPreview();
    } else if (selectionPurpose === 'BLOCK_MEDIA') {
        currentArticleData[selectionBlockIndex].content = path;
        renderEditor();
        renderPreview();
    } else if (selectionPurpose === 'CREATE_ARTICLE') {
        executeCreateArticle(selectionExtraData, path);
    } else if (selectionPurpose === 'MOVE_ARTICLE') {
        confirmMoveArticle(path);
    } else if (selectionPurpose === 'MOVE_FOLDER') {
        confirmMoveFolder(selectionExtraData, path);
    }
    cancelSelection();
}

function cancelSelection() {
    isSelectingInTree = false;
    selectionPurpose = '';
    selectionBlockIndex = -1;
    selectionType = '';
    selectionExtraData = null;
    document.getElementById('selection-popup').style.display = 'none';
}

async function loadArticle(path, title) {
    if (currentArticlePath) previousArticlePath = currentArticlePath;
    currentArticlePath = path;
    const response = await fetch(`api/article?path=${encodeURIComponent(path)}`);
    currentArticleData = await response.json();

    document.getElementById('current-article-name').textContent = title;
    document.getElementById('editor-actions').style.display = 'flex';
    document.getElementById('add-block-toolbar').style.display = 'flex';

    // Refresh the add block toolbar
    renderAddBlockToolbar();

    // Highlight in list
    document.querySelectorAll('#article-list .article-item').forEach(item => {
        item.classList.toggle('selected', item.dataset.path === path);
        item.classList.toggle('media-selected', item.dataset.path === previewedMediaPath);
    });

    renderEditor();
    renderPreview();
}

function renderAddBlockToolbar() {
    const toolbar = document.getElementById('add-block-toolbar');
    toolbar.innerHTML = '';
    const types = ["title", "icon", "header", "subheader", "paragraph", "image", "video", "link", "separator"];
    types.forEach(t => {
        const btn = document.createElement('button');
        btn.textContent = t.charAt(0).toUpperCase() + t.slice(1);
        btn.onclick = () => addSpecificBlock(t);
        toolbar.appendChild(btn);
    });
}

function addSpecificBlock(type) {
    if (type === 'title' && currentArticleData.some(b => b.type === 'title')) {
        alert("Article already has a title block.");
        return;
    }
    if (type === 'icon' && currentArticleData.some(b => b.type === 'icon')) {
        alert("Article already has an icon block.");
        return;
    }
    const newBlock = {type: type, content: ''};
    if (type === 'link') newBlock.target = '';
    if (type === 'title' || type === 'icon') {
        // Metadata blocks at the top
        currentArticleData.unshift(newBlock);
    } else {
        currentArticleData.push(newBlock);
    }
    renderEditor();
    renderPreview();
}

function renderEditor() {
    const list = document.getElementById('block-list');
    list.innerHTML = '';

    currentArticleData.forEach((block, index) => {
        const div = document.createElement('div');
        div.className = 'block-edit';

        const typeLabel = document.createElement('div');
        typeLabel.className = 'block-type-label';
        typeLabel.textContent = block.type;
        div.appendChild(typeLabel);

        const controls = document.createElement('div');
        controls.className = 'block-controls';
        controls.innerHTML = `
            <button onclick="moveBlock(${index}, -1)">↑</button>
            <button onclick="moveBlock(${index}, 1)">↓</button>
            <button class="danger" onclick="removeBlock(${index})">Delete</button>
        `;
        div.appendChild(controls);

        if (block.type === 'image' || block.type === 'video') {
            const entryRow = document.createElement('div');
            entryRow.style.display = 'flex';
            entryRow.style.gap = '5px';
            entryRow.style.marginBottom = '5px';

            const input = document.createElement('input');
            input.type = 'text';
            input.value = block.content;
            input.placeholder = 'Path to media...';
            input.style.flex = '1';
            input.oninput = (e) => {
                block.content = e.target.value;
                renderPreview();
            };
            entryRow.appendChild(input);

            const selectBtn = document.createElement('button');
            selectBtn.textContent = 'Select Existing Media';
            selectBtn.onclick = () => showMediaSelectorForBlock(index);
            entryRow.appendChild(selectBtn);

            const uploadBtn = document.createElement('button');
            uploadBtn.textContent = 'Upload Media...';
            uploadBtn.onclick = () => triggerUpload(index);
            entryRow.appendChild(uploadBtn);

            div.appendChild(entryRow);
        } else if (block.type === 'link') {
            const input = document.createElement('input');
            input.type = 'text';
            input.value = block.content;
            input.placeholder = 'Link text...';
            input.style.marginBottom = '5px';
            input.oninput = (e) => {
                block.content = e.target.value;
                renderPreview();
            };
            div.appendChild(input);

            const targetContainer = document.createElement('div');
            targetContainer.style.display = 'flex';
            targetContainer.style.gap = '5px';

            const targetInput = document.createElement('input');
            targetInput.type = 'text';
            targetInput.value = block.target;
            targetInput.placeholder = 'Target article path (relative)...';
            targetInput.style.flex = '1';
            targetInput.oninput = (e) => {
                block.target = e.target.value;
                renderPreview();
            };
            targetContainer.appendChild(targetInput);

            const selectBtn = document.createElement('button');
            selectBtn.textContent = 'Select...';
            selectBtn.onclick = () => showLinkSelectorForBlock(index);
            targetContainer.appendChild(selectBtn);

            div.appendChild(targetContainer);
        } else if (block.type === 'separator') {
            const label = document.createElement('div');
            label.textContent = '(Visual Separator)';
            label.style.fontStyle = 'italic';
            label.style.color = '#888';
            div.appendChild(label);
        } else {
            const textarea = document.createElement('textarea');
            textarea.value = block.content;
            textarea.rows = block.type === 'paragraph' ? 4 : 1;
            textarea.oninput = (e) => {
                block.content = e.target.value;
                renderPreview();
            };
            div.appendChild(textarea);
        }

        list.appendChild(div);
    });
}

function getDisplayPath(path) {
    if (!path) return "";
    return path.replace('help_window/help_content/', '')
        .replace('app/help_system/help_content/', '')
        .replace('help_system/help_content/', '');
}

function renderPreview() {
    const preview = document.getElementById('preview-content');
    preview.innerHTML = '';

    currentArticleData.forEach(block => {
        let el;
        switch (block.type) {
            case 'title':
                // Title is mandatory but we don't always render it in ArticleViewer
                // but for preview it's good to see.
                el = document.createElement('h1');
                el.className = 'preview-title';
                el.textContent = block.content;
                el.style.display = 'block';
                break;
            case 'icon':
                // Icon metadata not visible in article
                el = null;
                break;
            case 'header':
                el = document.createElement('h2');
                el.className = 'preview-header';
                el.textContent = block.content;
                break;
            case 'subheader':
                el = document.createElement('h3');
                el.className = 'preview-subheader';
                el.textContent = block.content;
                break;
            case 'paragraph':
                el = document.createElement('p');
                el.className = 'preview-paragraph';
                el.textContent = block.content;
                break;
            case 'image':
                el = document.createElement('img');
                el.className = 'preview-image';
                let src = getDisplayPath(block.content);
                el.src = `media/${src}`;
                break;
            case 'video':
                el = document.createElement('video');
                el.className = 'preview-video';
                el.controls = true;
                let vsrc = getDisplayPath(block.content);
                el.src = `media/${vsrc}`;
                break;
            case 'link':
                el = document.createElement('a');
                el.className = 'preview-link';
                el.textContent = block.content;
                let target = getDisplayPath(block.target);
                el.onclick = (e) => {
                    e.preventDefault();
                    if (target) {
                        loadArticle(target, block.content);
                    }
                };
                el.href = '#';
                break;
            case 'separator':
                el = document.createElement('hr');
                el.style.margin = '20px 0';
                el.style.border = '0';
                el.style.borderTop = '1px solid #eee';
                break;
        }
        if (el) preview.appendChild(el);
    });
}

function cancelEdit() {
    if (confirm("Are you sure you want to cancel? All unsaved changes will be lost.")) {
        if (currentArticlePath) {
            // Reload original
            loadArticle(currentArticlePath, document.getElementById('current-article-name').textContent);
        }
    }
}

async function consolidateMedia() {
    try {
        const response = await fetch('api/consolidate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({path: currentArticlePath, content: currentArticleData})
        });
        const result = await response.json();
        if (result.status === 'success') {
            if (result.changed) {
                currentArticleData = result.content;
                refreshArticleList();
                renderEditor();
                renderPreview();
                alert("Media consolidated successfully.");
            } else {
                alert("All media already consolidated.");
            }
        } else {
            alert("Error consolidating media: " + result.error);
        }
    } catch (e) {
        alert("Network error while consolidating media.");
    }
}

/* Modal and Dialogs */

function esc(str) {
    if (!str) return "";
    return JSON.stringify(str).replace(/"/g, '&quot;');
}

function showModal(title, bodyHtml, footerHtml) {
    const modal = document.getElementById('modal-overlay');
    const content = document.getElementById('modal-content');

    content.innerHTML = `
        <div class="modal-header">
            <h2 style="margin:0">${title}</h2>
            <button onclick="hideModal()">&times;</button>
        </div>
        <div class="modal-body">${bodyHtml}</div>
        <div class="modal-footer">${footerHtml || '<button onclick="hideModal()">Close</button>'}</div>
    `;

    modal.style.display = 'flex';
}

function hideModal() {
    document.getElementById('modal-overlay').style.display = 'none';

    // HLP-036.4: Selection reversion logic
    if (!currentArticlePath) {
        // Find help_for_help or first available
        findAndLoadDefaultArticle();
    }
}

async function findAndLoadDefaultArticle() {
    const response = await fetch('api/articles');
    const articles = await response.json();
    let target = articles.find(a => a.file_path.includes('help_for_help.json'));
    if (!target && articles.length > 0) target = articles[0];

    if (target) {
        loadArticle(target.file_path, target.title);
    }
}

async function showMediaBrowser(path) {
    const response = await fetch(`api/media_list?path=${encodeURIComponent(path)}`);
    const files = await response.json();

    let body = '<div class="media-grid">';
    files.forEach(file => {
        const isImage = /\.(jpg|jpeg|png|gif|bmp|webp)$/i.test(file.name);
        body += `
            <div class="media-item" onclick="previewMedia(${esc(file.url)}, ${esc(file.name)})">
                ${isImage ? `<img src="${file.url}">` : '<div style="height:60px; display:flex; align-items:center; justify-content:center; font-size:24px;">📄</div>'}
                <div>${file.name}</div>
            </div>
        `;
    });
    body += '</div>';

    showModal('Media Browser', body, '<button onclick="hideModal()">Close</button>');
}

function previewMedia(url, name) {
    const isImage = /\.(jpg|jpeg|png|gif|bmp|webp)$/i.test(name);
    let html = '';
    if (isImage) {
        html = `<img src="${url}" style="max-width:100%; border: 1px solid #ccc;">`;
    } else {
        html = `<p>Preview not available for this file type: ${name}</p>`;
    }

    // We can just alert or show another modal, but let's just alert for now or replace body
    showModal(`Preview: ${name}`, html, '<button onclick="hideModal()">Back</button>');
}

function showFolderOptions(folder) {
    const body = `
        <p>Folder: <strong>${folder.name}</strong></p>
        <div style="display: flex; flex-direction: column; gap: 10px;">
            <button onclick="renameFolderPrompt(${esc(folder.path)})">Rename Folder</button>
            <button onclick="moveFolderPrompt(${esc(folder.path)})">Move Folder</button>
            <button class="danger" onclick="deleteFolderPrompt(${esc(folder.path)})">Delete Folder</button>
            <button onclick="createNewFolderPrompt(${esc(folder.path)})">Create New Subfolder</button>
        </div>
    `;
    showModal('Folder Options', body);
}

async function moveFolderPrompt(path) {
    hideModal();

    isSelectingInTree = true;
    selectionPurpose = 'MOVE_FOLDER';
    selectionType = 'folder';
    selectionExtraData = path; // The folder we are moving

    const popup = document.getElementById('selection-popup');
    const title = document.getElementById('selection-popup-title');
    const msg = document.getElementById('selection-popup-message');
    const error = document.getElementById('selection-error');
    const pathDisplay = document.getElementById('selection-path-display');
    const okBtn = document.getElementById('selection-ok-btn');

    title.textContent = 'Move Folder';
    msg.textContent = 'Select target parent folder in the tree.';
    error.style.display = 'none';
    pathDisplay.textContent = 'No folder selected';
    okBtn.style.display = 'none';
    popup.style.display = 'block';
}

async function confirmMoveFolder(oldPath, newParentPath) {
    const response = await fetch('api/move', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({old_path: oldPath, new_parent: newParentPath})
    });
    if (response.ok) {
        hideModal();
        refreshArticleList();
    } else {
        const err = await response.json();
        alert("Error moving folder: " + err.error);
    }
}

async function renameFolderPrompt(path) {
    const newName = prompt("Enter new name:");
    if (!newName) return;

    const response = await fetch('api/rename', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({path, new_name: newName})
    });
    if (response.ok) {
        hideModal();
        refreshArticleList();
    } else {
        const err = await response.json();
        alert("Error renaming: " + err.error);
    }
}

async function deleteFolderPrompt(path) {
    if (confirm("Are you sure you want to delete this folder and all its contents?")) {
        const response = await fetch('api/delete', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({path})
        });
        if (response.ok) {
            hideModal();
            refreshArticleList();
        } else {
            const err = await response.json();
            alert("Error deleting: " + err.error);
        }
    }
}

async function createNewFolderPrompt(parentPath) {
    const name = prompt("Enter folder name:");
    if (!name) return;

    const response = await fetch('api/create_folder', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({parent_path: parentPath, name})
    });
    if (response.ok) {
        hideModal();
        refreshArticleList();
    } else {
        const err = await response.json();
        alert("Error creating folder: " + err.error);
    }
}

async function moveArticle() {
    if (!currentArticlePath) return;

    isSelectingInTree = true;
    selectionPurpose = 'MOVE_ARTICLE';
    selectionType = 'folder';

    const popup = document.getElementById('selection-popup');
    const title = document.getElementById('selection-popup-title');
    const msg = document.getElementById('selection-popup-message');
    const error = document.getElementById('selection-error');
    const pathDisplay = document.getElementById('selection-path-display');
    const okBtn = document.getElementById('selection-ok-btn');

    title.textContent = 'Move Article';
    msg.textContent = 'Select target destination folder in the tree.';
    error.style.display = 'none';
    pathDisplay.textContent = 'No folder selected';
    okBtn.style.display = 'none';
    popup.style.display = 'block';
}

async function confirmMoveArticle(newParentPath) {
    const response = await fetch('api/move', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({old_path: currentArticlePath, new_parent: newParentPath})
    });
    if (response.ok) {
        const result = await response.json();
        hideModal();
        currentArticlePath = result.new_path;
        await refreshArticleList();
        loadArticle(currentArticlePath, document.getElementById('current-article-name').textContent);
    } else {
        const err = await response.json();
        alert("Error moving: " + err.error);
    }
}

function removeBlock(index) {
    if (currentArticleData[index].type === 'title') {
        alert("Cannot delete mandatory title block.");
        return;
    }
    if (confirm("Are you sure you want to delete this block?")) {
        currentArticleData.splice(index, 1);
        renderEditor();
        renderPreview();
    }
}

function moveBlock(index, delta) {
    const newIndex = index + delta;
    if (newIndex < 0 || newIndex >= currentArticleData.length) return;

    // Title and Icon blocks must stay at the top
    if (currentArticleData[index].type === 'title' || currentArticleData[index].type === 'icon') return;
    if (currentArticleData[newIndex].type === 'title' || currentArticleData[newIndex].type === 'icon') return;

    const temp = currentArticleData[index];
    currentArticleData[index] = currentArticleData[newIndex];
    currentArticleData[newIndex] = temp;
    renderEditor();
    renderPreview();
}

async function saveCurrentArticle() {
    try {
        const response = await fetch('api/article', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({path: currentArticlePath, content: currentArticleData})
        });
        if (response.ok) {
            alert("Article saved successfully!");
            refreshArticleList();
        } else {
            const err = await response.json();
            alert("Error saving article: " + err.error);
        }
    } catch (e) {
        alert("Network error while saving article.");
    }
}

function triggerUpload(blockIndex) {
    const input = document.createElement('input');
    input.type = 'file';
    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);
        formData.append('article_path', currentArticlePath);

        try {
            const response = await fetch('api/upload_media', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            if (result.status === 'success') {
                currentArticleData[blockIndex].content = result.path;
                refreshArticleList();
                renderEditor();
                renderPreview();
            } else {
                alert("Upload failed: " + result.error);
            }
        } catch (e) {
            alert("Network error during upload.");
        }
    };
    input.click();
}

async function createNewArticle() {
    const title = prompt("Enter article title:");
    if (!title) return;

    isSelectingInTree = true;
    selectionPurpose = 'CREATE_ARTICLE';
    selectionType = 'folder';
    selectionExtraData = title;

    const popup = document.getElementById('selection-popup');
    const titleEl = document.getElementById('selection-popup-title');
    const msg = document.getElementById('selection-popup-message');
    const error = document.getElementById('selection-error');
    const pathDisplay = document.getElementById('selection-path-display');
    const okBtn = document.getElementById('selection-ok-btn');

    titleEl.textContent = 'New Article: ' + title;
    msg.textContent = 'Select destination folder in the tree.';
    error.style.display = 'none';
    pathDisplay.textContent = 'No folder selected';
    okBtn.style.display = 'none';
    popup.style.display = 'block';
}

async function executeCreateArticle(title, sectionPath) {
    const section = getDisplayPath(sectionPath);
    try {
        const response = await fetch('api/create_article', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({title, section})
        });
        const result = await response.json();
        if (response.ok) {
            await refreshArticleList();
            loadArticle(result.file_path, title);
        } else {
            alert("Error creating article: " + result.error);
        }
    } catch (e) {
        alert("Network error while creating article.");
    }
}

// Initial load
async function init() {
    const urlParams = new URLSearchParams(window.location.search);
    checkedOutVersionId = urlParams.get('checked_out');

    if (checkedOutVersionId) {
        document.getElementById('checkout-indicator').style.display = 'flex';
        document.getElementById('checked-out-version-id').textContent = 'Version ' + checkedOutVersionId;
    }

    await refreshArticleList();
}

function clearCheckout() {
    if (confirm("Clear checked-out version state? You will remain on the current draft content.")) {
        window.location.href = EDITOR_PAGE_URL;
    }
}

function goToPublishing() {
    let url = VERSIONING_PAGE_URL;
    if (checkedOutVersionId) {
        url += '?checked_out=' + checkedOutVersionId;
    }
    window.location.href = url;
}

init();
