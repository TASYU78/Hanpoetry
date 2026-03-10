import os
import tkinter as tk
import webbrowser
from tkinter import ttk, filedialog
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDFS
from collections import defaultdict

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")

class SKOSViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SKOS Tree Viewer")
        self.graph = Graph()
        self.broader_map = defaultdict(list)
        self.labels_map = defaultdict(dict)
        self.alt_labels = defaultdict(dict)
        self.concept_definitions = defaultdict(dict)
        self.concept_comments = defaultdict(dict)
        self.scheme_labels = defaultdict(dict)
        self.scheme_metadata = {}
        self.scheme_to_concepts = defaultdict(list)
        self.tree_items = {}
        self.jump_history = []
        self.forward_history = []
        self.recent_queries = []
        self.max_recent = 5
        self.loaded_files = []
        self.current_language = tk.StringVar(value='zh')
        self.setup_gui()

    def setup_gui(self):
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True)
        left = ttk.Frame(paned, width=400)
        paned.add(left)

        load_frame = ttk.Frame(left)
        load_frame.pack(fill='x', padx=4, pady=4)
        ttk.Button(load_frame, text="Open TTL Files", command=self.open_file).pack(side='left')

        self.file_list_frame = ttk.LabelFrame(left, text="Loaded Files", padding=(4,4))
        self.file_list_frame.pack(fill='x', padx=4, pady=4)

        search_frame = ttk.Frame(left)
        search_frame.pack(fill='x', padx=4, pady=4)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.bind("<Return>", lambda e: self.search_concept())
        ttk.Button(search_frame, text="Search", command=self.search_concept).pack(side='left', padx=2)
        ttk.Button(search_frame, text="Back", command=self.go_back).pack(side='left', padx=2)
        ttk.Button(search_frame, text="Forward", command=self.go_forward).pack(side='left', padx=2)

        lang_frame = ttk.Frame(left)
        lang_frame.pack(fill='x', padx=4, pady=(0,4))
        ttk.Label(lang_frame, text="Language:").pack(side='left')
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.current_language,
                                  values=["zh", "en", "ja"], width=3, state="readonly")
        lang_combo.pack(side='left')
        lang_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_tree())

        self.tree = ttk.Treeview(left)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.display_details)

        right = ttk.Frame(paned)
        paned.add(right)
        self.detail_text = tk.Text(right, wrap='word', state='disabled')
        self.detail_text.pack(fill="both", expand=True, padx=5, pady=5)

        self.recent_frame_container = ttk.LabelFrame(right, text="Recent", padding=(4,4))
        self.recent_frame_container.pack(fill='x', padx=5, pady=(0,4))
        self.recent_frame = ttk.Frame(self.recent_frame_container)
        self.recent_frame.pack(fill='x')

    def open_file(self):
        files = filedialog.askopenfilenames(filetypes=[("Turtle Files", "*.ttl")])
        for f in files:
            if f not in self.loaded_files:
                self.loaded_files.append(f)
        if self.loaded_files:
            self.reload_graph()
            self.build_data()
            self.refresh_tree()
            self.update_file_list_ui()

    def remove_file(self, fpath):
        if fpath in self.loaded_files:
            self.loaded_files.remove(fpath)
            self.reload_graph()
            self.build_data()
            self.refresh_tree()
            self.update_file_list_ui()

    def reload_graph(self):
        self.graph = Graph()
        for f in self.loaded_files:
            self.graph.parse(f, format='ttl')

    def update_file_list_ui(self):
        for w in self.file_list_frame.winfo_children():
            w.destroy()
        for f in self.loaded_files:
            name = os.path.basename(f)
            fr = ttk.Frame(self.file_list_frame)
            fr.pack(fill='x', pady=1)
            ttk.Label(fr, text=name).pack(side='left', fill='x', expand=True)
            ttk.Button(fr, text="Close", width=6, command=lambda ff=f: self.remove_file(ff)).pack(side='right')

    def build_data(self):
        self.broader_map.clear()
        self.labels_map.clear()
        self.alt_labels.clear()
        self.concept_definitions.clear()
        self.concept_comments.clear()
        self.scheme_labels.clear()
        self.scheme_to_concepts.clear()
        self.scheme_metadata.clear()
        self.tree_items.clear()

        implicit = set(self.graph.objects(predicate=SKOS.inScheme))
        for sch in implicit:
            if sch not in self.scheme_labels:
                label = str(sch).split('#')[-1]
                self.scheme_labels[sch] = {self.current_language.get(): label}
                self.scheme_metadata[sch] = {}

        seen = set()
        for s in self.graph.subjects():
            if not isinstance(s, URIRef) or s in seen:
                continue
            seen.add(s)
            if (s, None, SKOS.ConceptScheme) in self.graph:
                for lbl in self.graph.objects(s, SKOS.prefLabel):
                    if isinstance(lbl, Literal) and lbl.language:
                        self.scheme_labels[s][lbl.language] = str(lbl)
                meta = {}
                for key, prop in {'title': DCT.title, 'creator': DCT.creator, 'created': DCT.created}.items():
                    val = self.graph.value(s, prop)
                    if val:
                        meta[key] = str(val)
                self.scheme_metadata[s] = meta
                continue
            for lbl in self.graph.objects(s, SKOS.prefLabel):
                if isinstance(lbl, Literal) and lbl.language:
                    self.labels_map[s][lbl.language] = str(lbl)
            for lbl in self.graph.objects(s, SKOS.altLabel):
                if isinstance(lbl, Literal) and lbl.language:
                    self.alt_labels[s][lbl.language] = str(lbl)
            for d in self.graph.objects(s, SKOS.definition):
                if isinstance(d, Literal) and d.language:
                    self.concept_definitions[s][d.language] = str(d)
            for c in self.graph.objects(s, RDFS.comment):
                if isinstance(c, Literal) and c.language:
                    self.concept_comments[s][c.language] = str(c)
            for b in self.graph.objects(s, SKOS.broader):
                if isinstance(b, URIRef):
                    self.broader_map[b].append(s)
            for sch in self.graph.objects(s, SKOS.inScheme):
                if isinstance(sch, URIRef):
                    self.scheme_to_concepts[sch].append(s)

    def refresh_tree(self):
        lang = self.current_language.get()
        self.tree.delete(*self.tree.get_children())
        self.tree_items.clear()
        for sch in sorted(self.scheme_labels, key=lambda x: self.scheme_labels[x].get(lang, str(x))):
            label = self.scheme_labels[sch].get(lang, str(sch))
            item = self.tree.insert('', 'end', text=label, values=(str(sch),))
            self.tree_items[str(sch)] = item
            roots = [c for c in self.scheme_to_concepts.get(sch, [])
                     if c not in {ch for children in self.broader_map.values() for ch in children}]
            for c in sorted(roots, key=lambda x: self.get_label(x, lang)):
                self.build_tree(item, c, lang)
        all_ch = {ch for children in self.broader_map.values() for ch in children}
        all_in = {c for lst in self.scheme_to_concepts.values() for c in lst}
        indep = [n for n in self.labels_map if n not in all_ch and n not in all_in]
        for n in sorted(indep, key=lambda x: self.get_label(x, lang)):
            self.build_tree('', n, lang)

    def build_tree(self, parent, node, lang):
        label = self.get_label(node, lang)
        item = self.tree.insert(parent, 'end', text=label, values=(str(node),))
        self.tree_items[str(node)] = item
        for ch in sorted(self.broader_map.get(node, []), key=lambda x: self.get_label(x, lang)):
            self.build_tree(item, ch, lang)

    def get_label(self, node, lang):
        return self.labels_map[node].get(lang) or next(iter(self.labels_map[node].values()), str(node))

    def display_details(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        uri = self.tree.item(sel[0], 'values')[0]
        node = URIRef(uri)
        lines = [f"URI: {uri}"]
        if self.labels_map.get(node):
            labs = [f"{v} ({k})" for k,v in self.labels_map[node].items()]
            lines.append("prefLabel: " + "; ".join(labs))
        if self.alt_labels.get(node):
            labs = [f"{v} ({k})" for k,v in self.alt_labels[node].items()]
            lines.append("altLabel: " + "; ".join(labs))
        if self.concept_definitions.get(node):
            defs = [f"[{k}] {v}" for k,v in self.concept_definitions[node].items()]
            lines.append("Definition:")
            lines.extend(defs)
        if self.concept_comments.get(node):
            lines.append("Comment:")
            current_lang = self.current_language.get()
            for k, v in self.concept_comments[node].items():
                prefix = "★" if k == current_lang else " "
                lines.append(f"{prefix}[{k}] {v}")
        broader = list(self.graph.objects(node, SKOS.broader))
        narrower = list(self.graph.subjects(SKOS.broader, node))
        if broader:
            lines.append("Broader:")
            for o in broader:
                lines.append(f"- {self.get_label(o, self.current_language.get())} ({o})")
        if narrower:
            lines.append("Narrower:")
            for o in narrower:
                lines.append(f"- {self.get_label(o, self.current_language.get())} ({o})")
        content = "\n".join(lines)
        self.detail_text.config(state='normal')
        self.detail_text.delete('1.0', tk.END)
        self.detail_text.insert(tk.END, content)
        self.detail_text.config(state='disabled')

    def search_concept(self):
        q = self.search_entry.get().strip().lower()
        if not q:
            return
        lang = self.current_language.get()
        matches = []
        for node, labs in self.labels_map.items():
            if any(q in v.lower() for v in labs.values()) or q in str(node).lower():
                label = self.get_label(node, lang)
                matches.append((label, node))
        if not matches:
            return
        elif len(matches) == 1:
            self.jump_to_concept(matches[0][1])
        else:
            top = tk.Toplevel(self.root)
            top.title("Select a concept")
            top.geometry("300x250")
            tk.Label(top, text="Select a match:").pack(pady=4)
            lb = tk.Listbox(top, height=12)
            lb.pack(fill='both', expand=True, padx=8)
            for label, node in matches:
                lb.insert(tk.END, f"{label} ({str(node).split('#')[-1]})")
            def on_select():
                index = lb.curselection()
                if index:
                    selected_node = matches[index[0]][1]
                    self.jump_to_concept(selected_node)
                    top.destroy()
            btn = ttk.Button(top, text="Go", command=on_select)
            btn.pack(pady=6)
            lb.bind("<Double-Button-1>", lambda e: on_select())

    def go_back(self):
        if self.jump_history:
            prev = self.jump_history.pop()
            self.jump_to_concept(prev)

    def go_forward(self):
        if self.forward_history:
            nxt = self.forward_history.pop()
            self.jump_to_concept(nxt)

    def open_external_link(self, uri):
        webbrowser.open(str(uri))

    def jump_to_concept(self, node):
        u = str(node)
        if self.tree_items.get(u) is None:
            return
        selected = self.tree.selection()
        if selected:
            current_uri = self.tree.item(selected[0], 'values')[0]
            if current_uri == u:
                return
        item = self.tree_items[u]
        self.tree.see(item)
        self.tree.selection_set(item)

        # 只在跳转时更新 recent
        if u in self.recent_queries:
            self.recent_queries.remove(u)
        self.recent_queries.insert(0, u)
        if len(self.recent_queries) > self.max_recent:
            self.recent_queries.pop()
        for w in self.recent_frame.winfo_children():
            w.destroy()
        for uri in self.recent_queries:
            lab = self.get_label(URIRef(uri), self.current_language.get())
            txt = lab[:6] + '…' if len(lab) > 6 else lab
            btn = ttk.Button(self.recent_frame, text=txt, command=lambda uu=uri: self.jump_to_concept(uu))
            btn.pack(side='left', padx=2)

        self.display_details()

if __name__ == '__main__':
    root = tk.Tk()
    app = SKOSViewerApp(root)
    root.mainloop()
