import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


class Report:

    def save_file(
        self, extenstion, results_df, diffed_output_path, remove_gene_id=False
    ):
        if remove_gene_id:
            results_df = results_df.drop(columns=["gene_id"])

        print("writing into file...")

        if extenstion == "csv":
            ouput_path_csv = diffed_output_path

            results_df.to_csv(ouput_path_csv, sep=",")

        if extenstion == "tsv":
            ouput_path_csv = diffed_output_path

            results_df.to_csv(ouput_path_csv, sep="\t")

        print(f"File done! The file can be finded in {ouput_path_csv}")

    def save_volcano(self, classificated_df, output_volcano_path):

        volcano_df = classificated_df

        volcano_df["-log10(padj)"] = -np.log10(classificated_df["padj"])

        plt.figure(figsize=(10, 6))
        sns.set(style="whitegrid")

        sns.scatterplot(
            data=volcano_df,
            x="log2FoldChange",
            y="-log10(padj)",
            hue="significance",
            palette={"UP": "red", "DOWN": "blue", "NOT_SIGNIFICANT": "gray"},
            edgecolor=None,
        )

        plt.xlabel("Log2 Fold Change")
        plt.ylabel("-Log10(p-value adjusted)")
        plt.title("Volcano Plot of Differential Expression")

        plt.legend(title="Gene Regulation")

        plt.savefig(f"{output_volcano_path}")

        print(f"Image done! Can be finded in {output_volcano_path}")
