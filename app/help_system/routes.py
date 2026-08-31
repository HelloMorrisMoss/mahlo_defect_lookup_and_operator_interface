import difflib
import json
import os

from flask import render_template, jsonify, request, send_from_directory, current_app
from flask_login import login_required

from app.help_system import help_system_bp
from app.help_system.editor.file_manager import upload_media, delete_resource, rename_resource, move_resource, \
    consolidate_article_media
from app.help_system.utils.article_processor import ensure_article_integrity
from app.help_system.utils.cas_manager import CASManager
from app.models import ContentVersion, db


# Initialize CASManager lazily or via a property
def get_cas_manager():
    content_dir = os.path.join(current_app.root_path, 'help_system', 'help_content')
    return CASManager(content_dir)

def to_abs(path):
    content_dir = os.path.join(current_app.root_path, 'help_system', 'help_content')
    return os.path.abspath(os.path.join(content_dir, path))

def to_rel(path):
    content_dir = os.path.join(current_app.root_path, 'help_system', 'help_content')
    return os.path.relpath(path, content_dir).replace("\\", "/")

@help_system_bp.route('/editor')
@login_required
def web_editor():
    return render_template('web_editor.html')

@help_system_bp.route('/api/articles')
@login_required
def get_articles():
    content_dir = os.path.join(current_app.root_path, 'help_system', 'help_content')
    articles = []
    for root, dirs, files in os.walk(content_dir):
        if "blobs" in dirs:
            dirs.remove("blobs")
        if "staging" in dirs:
            dirs.remove("staging")
            
        for file in files:
            if file.endswith(".json") and file != "manifest.json":
                rel_path = to_rel(os.path.join(root, file))
                abs_path = os.path.join(root, file)
                title = "Untitled"
                icon = None
                try:
                    with open(abs_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list) and len(data) > 0:
                            for block in data:
                                if block.get('type') == 'title':
                                    title = block.get('content', 'Untitled')
                                elif block.get('type') == 'icon':
                                    icon = block.get('content')
                except Exception:
                    pass

                section = os.path.dirname(rel_path).replace("\\", "/")
                if section == ".": section = ""

                articles.append({
                    "file_path": rel_path,
                    "title": title,
                    "icon": icon,
                    "section": section
                })
    return jsonify(articles)

@help_system_bp.route('/api/structure')
@login_required
def get_structure():
    content_dir = os.path.join(current_app.root_path, 'help_system', 'help_content')
    def build_tree(current_dir):
        node_name = os.path.basename(current_dir) or "Root"
        tree = {
            "name": node_name,
            "type": "folder",
            "children": [],
            "path": to_rel(current_dir),
            "is_media": node_name == "media"
        }

        if tree["is_media"]:
            try:
                tree["item_count"] = len(
                    [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))])
            except Exception:
                tree["item_count"] = 0

        try:
            items = os.listdir(current_dir)
        except Exception:
            return tree
        
        for item in items:
            if item in ["blobs", "manifest.json", "staging"] or item.endswith(".lock"):
                continue
            abs_path = os.path.join(current_dir, item)
            if os.path.isdir(abs_path):
                tree["children"].append(build_tree(abs_path))
            else:
                if not item.endswith(".json"):
                    ext = item.lower().split('.')[-1]
                    media_type = "media"
                    if ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']:
                        media_type = "image"
                    elif ext in ['mp4', 'webm', 'ogg', 'mov', 'avi']:
                        media_type = "video"

                    tree["children"].append({
                        "name": item,
                        "type": media_type,
                        "path": to_rel(abs_path)
                    })
                else:
                    # Extract title and icon from article
                    title = item
                    icon = None
                    try:
                        with open(abs_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                for block in data:
                                    if block.get('type') == 'title':
                                        title = block.get('content', item)
                                    elif block.get('type') == 'icon':
                                        icon = block.get('content')
                    except Exception:
                        pass

                    tree["children"].append({
                        "name": title,
                        "type": "article",
                        "icon": icon,
                        "path": to_rel(abs_path)
                    })
        return tree
    
    return jsonify(build_tree(content_dir))

@help_system_bp.route('/api/article', methods=['GET'])
@login_required
def get_article_content():
    path = request.args.get('path')
    abs_path = to_abs(path)
    if not os.path.exists(abs_path):
        return jsonify({"error": "Article not found"}), 404
    with open(abs_path, 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

@help_system_bp.route('/api/article', methods=['POST'])
@login_required
def save_article():
    data = request.json
    path = data.get('path')
    content = data.get('content')

    # Enforce structural integrity (HLP-021)
    title = os.path.basename(path).replace(".json", "")
    content = ensure_article_integrity(content, title)
    
    abs_path = to_abs(path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2)
    return jsonify({"success": True})

@help_system_bp.route('/api/versions/history')
@login_required
def get_version_history():
    versions = ContentVersion.query.order_by(ContentVersion.timestamp.desc()).all()
    return jsonify([v.to_dict() for v in versions])

@help_system_bp.route('/api/versions/create', methods=['POST'])
@login_required
def create_version():
    data = request.json
    comment = data.get('comment', '')
    parent_id = data.get('parent_id')
    cas_manager = get_cas_manager()
    manifest_hash, manifest = cas_manager.create_manifest()
    new_version = ContentVersion(
        comment=comment,
        manifest_hash=manifest_hash,
        parent_id=parent_id
    )
    db.session.add(new_version)
    db.session.commit()
    return jsonify(new_version.to_dict())

@help_system_bp.route('/api/versions/publish', methods=['POST'])
@login_required
def publish_version():
    data = request.json
    version_id = data.get('id')
    ContentVersion.query.update({ContentVersion.is_published: False})
    version = db.session.get(ContentVersion, version_id)
    if version:
        version.is_published = True
        db.session.commit()
        return jsonify(version.to_dict())
    return jsonify({"error": "Version not found"}), 404


@help_system_bp.route('/api/versions/checkout', methods=['POST'])
@login_required
def checkout_version():
    data = request.json
    version_id = data.get('id')
    version = db.session.get(ContentVersion, version_id)
    if not version:
        return jsonify({"error": "Version not found"}), 404
    cas_manager = get_cas_manager()
    try:
        cas_manager.restore_from_manifest(version.manifest_hash)
        return jsonify({"success": True, "message": f"Version {version_id} checked out."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@help_system_bp.route('/api/versions/diff/<int:version_id>')
@login_required
def get_version_diff(version_id):
    version = db.session.get(ContentVersion, version_id)
    if not version:
        return jsonify({"error": "Version not found"}), 404
    prev_version = ContentVersion.query.filter(ContentVersion.timestamp < version.timestamp).order_by(
        ContentVersion.timestamp.desc()).first()
    cas_manager = get_cas_manager()
    current_manifest_path = cas_manager.get_blob_path(version.manifest_hash)
    try:
        with open(current_manifest_path, 'r', encoding='utf-8') as f:
            current_manifest = json.load(f)
    except Exception:
        return jsonify({"error": "Manifest not found or invalid"}), 500
    if prev_version:
        prev_manifest_path = cas_manager.get_blob_path(prev_version.manifest_hash)
        try:
            with open(prev_manifest_path, 'r', encoding='utf-8') as f:
                prev_manifest = json.load(f)
        except Exception:
            prev_manifest = {"files": {}}
    else:
        prev_manifest = {"files": {}}
    diff = {"added": [], "modified": [], "removed": []}
    curr_files = current_manifest.get("files", {})
    prev_files = prev_manifest.get("files", {})
    for path, file_hash in curr_files.items():
        if path not in prev_files:
            diff["added"].append({"path": path, "hash": file_hash})
        elif prev_files[path] != file_hash:
            diff["modified"].append({"path": path, "old_hash": prev_files[path], "new_hash": file_hash})
    for path, file_hash in prev_files.items():
        if path not in curr_files:
            diff["removed"].append({"path": path, "hash": file_hash})
    return jsonify(diff)

@help_system_bp.route('/api/versions/file_diff')
@login_required
def get_file_diff():
    old_hash = request.args.get('old_hash')
    new_hash = request.args.get('new_hash')
    path = request.args.get('path', '')
    if not path.lower().endswith(('.json', '.txt')):
        return jsonify({"diff": None})
    cas_manager = get_cas_manager()
    def get_content(h):
        if not h: return ""
        blob_path = cas_manager.get_blob_path(h)
        if os.path.exists(blob_path):
            try:
                with open(blob_path, 'r', encoding='utf-8') as f:
                    if path.endswith('.json'):
                        return json.dumps(json.load(f), indent=2)
                    return f.read()
            except Exception:
                return "[Binary Content or Encoding Error]"
        return ""
    old_content = get_content(old_hash)
    new_content = get_content(new_hash)
    diff = difflib.unified_diff(old_content.splitlines(), new_content.splitlines(), lineterm='')
    return jsonify({"diff": '\n'.join(list(diff))})

@help_system_bp.route('/versioning')
@login_required
def versioning_page():
    return render_template('versioning.html')


@help_system_bp.route('/api/upload_media', methods=['POST'])
@login_required
def web_upload_media():
    article_path = request.form.get('article_path')
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Temporarily save the file to a secure location or just use current_app.root_path
    from werkzeug.utils import secure_filename
    filename = secure_filename(file.filename)
    temp_path = os.path.join(current_app.root_path, 'help_system', 'flask_server_files', 'static', filename)
    file.save(temp_path)
    
    project_root = current_app.root_path
    try:
        rel_path = upload_media(project_root, to_abs(article_path), temp_path)
        return jsonify({"status": "success", "path": rel_path})
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@help_system_bp.route('/media/<path:filename>')
def serve_media(filename):
    content_dir = os.path.join(current_app.root_path, 'help_system', 'help_content')
    return send_from_directory(content_dir, filename)

@help_system_bp.route('/api/blob/<hash>')
@login_required
def get_blob(hash):
    cas_manager = get_cas_manager()
    blob_path = cas_manager.get_blob_path(hash)
    if os.path.exists(blob_path):
        return send_from_directory(cas_manager.blobs_dir, hash)
    return jsonify({"error": "Blob not found"}), 404


@help_system_bp.route('/api/media_list')
@login_required
def get_media_list():
    article_path = request.args.get('path')
    project_root = current_app.root_path
    from app.help_system.editor.file_manager import get_media_dir
    media_dir = get_media_dir(project_root, to_abs(article_path))
    media_files = []
    if os.path.exists(media_dir):
        for file in os.listdir(media_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4')):
                rel_path = to_rel(os.path.join(media_dir, file))
                media_files.append({
                    "name": file,
                    "path": rel_path,
                    "url": f"media/{rel_path}"
                })
    return jsonify(media_files)


@help_system_bp.route('/api/create_folder', methods=['POST'])
@login_required
def create_folder():
    data = request.json
    parent_path = data.get('parent_path', '')
    name = data.get('name')
    abs_path = os.path.join(to_abs(parent_path), name)
    os.makedirs(abs_path, exist_ok=True)
    return jsonify({"success": True, "path": to_rel(abs_path)})

@help_system_bp.route('/api/move', methods=['POST'])
@login_required
def web_move_resource():
    data = request.json
    project_root = current_app.root_path
    old_abs = to_abs(data.get('old_path'))
    new_parent_path = data.get('new_parent_path') or data.get('new_parent')
    new_parent_abs = to_abs(new_parent_path)
    new_abs = move_resource(project_root, old_abs, new_parent_abs)
    return jsonify({"success": True, "new_path": to_rel(new_abs)})

@help_system_bp.route('/api/rename', methods=['POST'])
@login_required
def web_rename_resource():
    data = request.json
    project_root = current_app.root_path
    old_path = data.get('old_path') or data.get('path')
    old_abs = to_abs(old_path)
    new_name = data.get('new_name')
    new_abs = rename_resource(project_root, old_abs, new_name)
    return jsonify({"success": True, "new_path": to_rel(new_abs)})

@help_system_bp.route('/api/delete', methods=['POST'])
@login_required
def web_delete_resource():
    data = request.json
    project_root = current_app.root_path
    abs_path = to_abs(data.get('path'))
    delete_resource(project_root, abs_path)
    return jsonify({"success": True})

@help_system_bp.route('/api/consolidate', methods=['POST'])
@login_required
def web_consolidate():
    data = request.json
    path = data.get('path')
    abs_path = to_abs(path)
    project_root = current_app.root_path
    with open(abs_path, 'r', encoding='utf-8') as f:
        article_data = json.load(f)
    new_data, changed = consolidate_article_media(project_root, abs_path, article_data)
    if changed:
        with open(abs_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, indent=2)
    return jsonify({"success": True, "changed": changed})


@help_system_bp.route('/api/create_article', methods=['POST'])
@login_required
def create_article():
    data = request.json
    title = data.get('title', 'New Article')
    section = data.get('section', '')

    # Generate filename from title
    import re
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().lower()
    safe_title = re.sub(r'[-\s]+', '-', safe_title)
    filename = f"{safe_title}.json"

    rel_path = os.path.join(section, filename).replace("\\", "/")
    abs_path = to_abs(rel_path)
    
    if os.path.exists(abs_path):
        # Add a number if it exists
        base, ext = os.path.splitext(rel_path)
        i = 1
        while os.path.exists(to_abs(f"{base}_{i}{ext}")):
            i += 1
        rel_path = f"{base}_{i}{ext}"
        abs_path = to_abs(rel_path)
    
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    initial_data = [
        {"type": "title", "content": title},
        {"type": "paragraph", "content": "Start writing your article here..."}
    ]
    with open(abs_path, 'w', encoding='utf-8') as f:
        json.dump(initial_data, f, indent=2)
    return jsonify({"success": True, "file_path": rel_path})
