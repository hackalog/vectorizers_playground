import numpy as np
from sklearn.neighbors import NearestNeighbors, KernelDensity
from matplotlib.colors import rgb2hex, Normalize
from IPython.display import display, HTML
import wordcloud
import umap
import matplotlib.pyplot as plt


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
    return fig

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
    return fig
