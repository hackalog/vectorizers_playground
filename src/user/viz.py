import numpy as np
from sklearn.neighbors import NearestNeighbors, KernelDensity
from matplotlib.colors import rgb2hex, Normalize
from IPython.display import display, HTML
import wordcloud
import hdbscan
import umap
import matplotlib.pyplot as plt
import pynndescent


def topic_word_by_class(
    doc_vectors,
    word_vectors,
    class_labels,
    class_names,
    index_to_word_fn,
    color_key,
    n_neighbors=150,
        random_state=42,
    background="white",
):
    unique_classes = np.unique(class_labels)
    word_nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine").fit(word_vectors)
    class_centroids = [np.mean(doc_vectors[class_labels == label], axis=0) for label in unique_classes]
    topic_word_dists, topic_word_indices = word_nbrs.kneighbors(class_centroids)
    umap_embedding = umap.UMAP(metric="cosine", random_state=random_state).fit_transform(doc_vectors)

    fig, ax = plt.subplots(figsize=(16,16))

    xmin, xmax = np.min(umap_embedding.T[0]), np.max(umap_embedding.T[0])
    ymin, ymax = np.min(umap_embedding.T[1]), np.max(umap_embedding.T[1])
    xs = np.linspace(xmin, xmax, 1024)
    ys = np.linspace(ymin, ymax, 1024)
    xv, yv = np.meshgrid(xs, ys[::-1])
    for_scoring = np.vstack([xv.ravel(), yv.ravel()]).T

    for i, label in enumerate(unique_classes):
        topic_words_and_freqs = {index_to_word_fn(idx):(1.0 - topic_word_dists[i, j])
                                 for j, idx in enumerate(topic_word_indices[i])}

        class_kde = KernelDensity(bandwidth=0.2, kernel="gaussian").fit(umap_embedding[class_labels == label])
        zv = class_kde.score_samples(for_scoring).reshape(xv.shape)
        mask = (np.exp(zv) < 2e-2) * 0xff
        level_colors = [color_key[class_names[label]] + alpha for alpha in ("00", "22", "44", "66", "88")]
        contour_data = np.exp(zv)
        ax.contourf(
            contour_data,
            levels=4,
            colors=level_colors,
            extent=(xmin, xmax, ymin, ymax),
            origin="upper",
            antialiased=True,
            zorder=0,
        )
        ax.scatter(
            *umap_embedding[class_labels == label].T,
            s=1.5,
            c=color_key[class_names[label]],
            alpha=0.25,
            linewidth=0,
            zorder=1
        )


        color_func = lambda *args, **kwargs: color_key[class_names[label]]
        wc = wordcloud.WordCloud(
            mode="RGBA",
            relative_scaling=1,
            min_font_size=1,
            max_font_size=64,
            background_color=None,
            color_func=color_func,
            mask=mask,
        )
        wc.fit_words(topic_words_and_freqs)
        ax.imshow(wc, extent=(xmin, xmax, ymin, ymax), zorder=2)

    ax.set(xticks=[], yticks=[], facecolor=background)
    return

def topic_word_by_cluster(
    doc_vectors,
    word_vectors,
    cluster_labels,
    index_to_word_fn,
    color_key,
    n_neighbors=150,
    background="white",
    kernel_bandwidth=0.2,
    kernel="gaussian"
):
    unique_clusters = np.unique(cluster_labels)
    unique_clusters = unique_clusters[unique_clusters >= 0]
    word_nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine").fit(word_vectors)
    cluster_centroids = [np.mean(doc_vectors[cluster_labels == label], axis=0) for label in unique_clusters]
    topic_word_dists, topic_word_indices = word_nbrs.kneighbors(cluster_centroids)
    umap_embedding = umap.UMAP(metric="cosine", random_state=42).fit_transform(doc_vectors)

    fig, ax = plt.subplots(figsize=(16,16))

    xmin, xmax = np.min(umap_embedding.T[0]), np.max(umap_embedding.T[0])
    ymin, ymax = np.min(umap_embedding.T[1]), np.max(umap_embedding.T[1])
    xs = np.linspace(xmin, xmax, 1024)
    ys = np.linspace(ymin, ymax, 1024)
    xv, yv = np.meshgrid(xs, ys[::-1])
    for_scoring = np.vstack([xv.ravel(), yv.ravel()]).T

    for i, label in enumerate(unique_clusters):
        topic_words_and_freqs = {index_to_word_fn(idx):(1.0 - topic_word_dists[i, j])
                                 for j, idx in enumerate(topic_word_indices[i])}

        class_kde = KernelDensity(bandwidth=kernel_bandwidth, kernel=kernel).fit(umap_embedding[cluster_labels == label])
        zv = class_kde.score_samples(for_scoring).reshape(xv.shape)
        mask = (np.exp(zv) < 2e-2) * 0xff
        level_colors = [color_key[label] + alpha for alpha in ("00", "22", "44", "66", "88")]
        contour_data = np.exp(zv)
        ax.contourf(
            contour_data,
            levels=4,
            colors=level_colors,
            extent=(xmin, xmax, ymin, ymax),
            origin="upper",
            antialiased=True,
            zorder=0,
        )
        ax.scatter(
            *umap_embedding[cluster_labels == label].T,
            s=1.5,
            c=color_key[label],
            alpha=0.25,
            linewidth=0,
            zorder=1
        )


        color_func = lambda *args, **kwargs: color_key[label]
        wc = wordcloud.WordCloud(
            mode="RGBA",
            relative_scaling=1,
            min_font_size=1,
            max_font_size=64,
            background_color=None,
            color_func=color_func,
            mask=mask,
        )
        wc.fit_words(topic_words_and_freqs)
        ax.imshow(wc, extent=(xmin, xmax, ymin, ymax), zorder=2)

    ax.set(xticks=[], yticks=[], facecolor=background)
    return

def document_cluster_tree(doc_vectors, min_cluster_size=50):
    low_dim_rep = umap.UMAP(
        metric="cosine", n_components=5, min_dist=1e-4, random_state=42, n_epochs=500
    ).fit_transform(doc_vectors)
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size).fit(low_dim_rep)
    tree = clusterer.condensed_tree_.to_pandas()
    return tree

def get_points(tree, cluster_id):
    child_rows = tree[tree.parent == cluster_id]
    result_points = []
    result_lambdas = []
    for i, row in child_rows.iterrows():
        if row.child_size == 1:
            result_points.append(int(row.child))
            result_lambdas.append(row.lambda_val)
        else:
            points, lambdas = get_points(tree, row.child)
            result_points.extend(points)
            result_lambdas.extend(lambdas)
    return result_points, result_lambdas

def get_topic_words(tree, cluster_id, vectors, nn_index, index_to_word_fn):
    row_ids, weights = get_points(tree, cluster_id)
    centroid = np.mean(vectors[row_ids], axis=0)
    if pynndescent.distances.cosine(centroid, np.mean(vectors, axis=0)) < 0.2:
        dists, inds = nn_index.kneighbors([centroid])
        return ["☼Generic☼"], [np.mean(dists)], len(row_ids)
    dists, inds = nn_index.kneighbors([centroid])
    keywords = [index_to_word_fn(x) for x in inds[0]]
    return keywords, dists[0], len(row_ids)

def topic_word_tree_recursion(tree, cluster_id, vectors, nn_index, index_to_word_fn, color_mapper):
    topic_words, topic_word_dists, size = get_topic_words(tree, cluster_id, vectors, nn_index, index_to_word_fn)
    child_rows = tree[tree.parent == cluster_id]
    child_rows = child_rows[child_rows.child_size > 1]
    topic_word_label = ""
    for j, word in enumerate(topic_words):
        topic_word_label += f"<font color='{rgb2hex(color_mapper.to_rgba(topic_word_dists[j]))}'>{word}</font> "

    if len(child_rows) > 0:
        result = f"<li><span class='caret'>{topic_word_label}</span>\n<ul class='nested'>\n"
        for i, row in child_rows.iterrows():
            result += topic_word_tree_recursion(tree, int(row.child), vectors, nn_index, index_to_word_fn, color_mapper)
        result += "</ul>"
    else:
        result = f"<li>■─ {topic_word_label}</li>"

    return result

def topic_word_tree(doc_vectors, word_vectors, index_to_word_fn, min_cluster_size=50, n_neighbors=5, min_dist=0.1, max_dist=0.5):
    tree = document_cluster_tree(doc_vectors, min_cluster_size=min_cluster_size)
    word_nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine").fit(word_vectors)
    color_norm = Normalize(vmin=min_dist, vmax=max_dist)
    color_mapper = plt.cm.ScalarMappable(norm=color_norm, cmap="viridis")
    tree_root = tree.parent.min()
    tree_html = topic_word_tree_recursion(tree, tree_root, doc_vectors, word_nbrs, index_to_word_fn, color_mapper)
    result = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {{
  height: 100ex;
  font-family: Tahoma, Verdana, sans-serif;
}}
ul, #myUL {{
  list-style-type: none;
}}
#myUL {{
  margin: 0;
  padding: 0;
}}
.caret {{
  cursor: pointer;
  user-select: none;
}}
.caret::before {{
  content: "►";
  color: black;
  display: inline-block;
  margin-right: 6px;
}}
.caret-down::before {{
  transform: rotate(90deg);
}}
.nested {{
  display: none;
}}
.active {{
  display: block;
}}
</style>
</head>
<body>
<ul id="myUL">
{tree_html}
</ul>
<script>
var toggler = document.getElementsByClassName("caret");
var i;
for (i = 0; i < toggler.length; i++) {{
  toggler[i].addEventListener("click", function() {{
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("caret-down");
  }});
}}
</script>
</body>
</html>
"""
    return HTML(result, metadata=dict(isolated=True))
