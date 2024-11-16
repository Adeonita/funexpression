import pandas as pd
from pandas import DataFrame

from pydeseq2.ds import DeseqStats
from pydeseq2.dds import DeseqDataSet
from pydeseq2.default_inference import DefaultInference

from ports.infrastructure.differ.differ_port import DifferPort


class DESeq2Adapter(DifferPort):
    def differ(self, pipeline_id: str, sra_files: dict, diffed_output_paths: dict):
        file_path_tri_control_1 = sra_files["control"]["srr_1"]
        file_path_tri_control_2 = sra_files["control"]["srr_2"]
        file_path_tri_control_3 = sra_files["control"]["srr_3"]

        file_path_tri_experiment_1 = sra_files["experiment"]["srr_1"]
        file_path_tri_experiment_2 = sra_files["experiment"]["srr_2"]
        file_path_tri_experiment_3 = sra_files["experiment"]["srr_3"]

        dataframe_control_1 = self._parse_counted_txt_to_dataframe(
            file_path_tri_control_1
        )
        dataframe_control_2 = self._parse_counted_txt_to_dataframe(
            file_path_tri_control_2
        )
        dataframe_control_3 = self._parse_counted_txt_to_dataframe(
            file_path_tri_control_3
        )

        dataframe_experiment_1 = self._parse_counted_txt_to_dataframe(
            file_path_tri_experiment_1
        )
        dataframe_experiment_2 = self._parse_counted_txt_to_dataframe(
            file_path_tri_experiment_2
        )
        dataframe_experiment_3 = self._parse_counted_txt_to_dataframe(
            file_path_tri_experiment_3
        )

        counted_df = self._build_counted_df(
            dataframe_control_1,
            dataframe_control_2,
            dataframe_control_3,
            dataframe_experiment_1,
            dataframe_experiment_2,
            dataframe_experiment_3,
            with_gene_id=False,
        )

        metadata = self._build_metadata_conditions()

        results_df = self._generate_deseq_from_counted_df(counted_df, metadata)

        classificated_df = self._add_significance_to_dataframe(results_df)

        self._save_file(
            extenstion="csv",
            results_df=classificated_df,
            diffed_output_path=diffed_output_paths.get("csv_file"),
        )
        # results_df_t = self._generate_deseq_from_counted_df(counts_df, metadata)

    def _parse_counted_txt_to_dataframe(self, file_path: str):
        df = pd.read_csv(file_path, sep="\t", header=None)

        return df.rename(columns={0: "gene_id", 1: "value"})

    def _save_file(self, extenstion, results_df, diffed_output_path):
        print("writing into file...")

        if extenstion == "csv":
            ouput_path_csv = diffed_output_path
            print("output path", ouput_path_csv)
            print("diffed_output_path", diffed_output_path)

            results_df.to_csv(ouput_path_csv, sep="\t")

        print(f"writing done, the file can be finded in {ouput_path_csv}")

    def _build_metadata_conditions(self):
        return pd.DataFrame(
            {
                "condition": [
                    "control",
                    "control",
                    "control",
                    "experiment",
                    "experiment",
                    "experiment",
                ]
            },
            index=[
                "control_sample_1",
                "control_sample_2",
                "control_sample_3",
                "experiment_sample_1",
                "experiment_sample_2",
                "experiment_sample_3",
            ],
        )

    def _build_counted_df(
        self,
        dataframe_control_1,
        dataframe_control_2,
        dataframe_control_3,
        dataframe_experiment_1,
        dataframe_experiment_2,
        dataframe_experiment_3,
        with_gene_id=False,
    ):
        # Manipulação necessária para remover as linhas informativas retornadas pelo arquivo contado
        # Não causa erro mas gera warning
        gene_id = dataframe_control_1[
            dataframe_control_1["gene_id"].str.contains("PDE")
        ]
        gene_id = gene_id["gene_id"]

        counts_df = pd.DataFrame()
        counts_df["index"] = gene_id
        counts_df["control_sample_1"] = dataframe_control_1["value"]
        counts_df["control_sample_2"] = dataframe_control_2["value"]
        counts_df["control_sample_3"] = dataframe_control_3["value"]

        counts_df["experiment_sample_1"] = dataframe_experiment_1["value"]
        counts_df["experiment_sample_2"] = dataframe_experiment_2["value"]
        counts_df["experiment_sample_3"] = dataframe_experiment_3["value"]

        if with_gene_id:
            counts_df["gene_id"] = gene_id

        counts_df = counts_df.set_index("index")

        return counts_df.T

    def _generate_deseq_from_counted_df(self, counts_df, metadata):
        inference = DefaultInference(n_cpus=8)

        deseq_dataset = DeseqDataSet(
            counts=counts_df,
            metadata=metadata,
            design_factors="condition",
            refit_cooks=True,
            inference=inference,
        )

        deseq_dataset.deseq2()

        stat_res = DeseqStats(deseq_dataset, inference=inference)
        stat_res.summary()

        results_df = (
            stat_res.results_df
        )  # para pegar o resultado preciso do summary sim, sem ele gera o erro "'DeseqStats' object has no attribute 'results_df'"

        # stat_res.results_df.to_csv(os.path.join(OUTPUT_PATH, "results.csv")) #gera um csv e escreve os resultados neste arquivo

        results_df["gene_id"] = results_df.index

        return results_df

    def _add_significance_to_dataframe(self, diffed_dataframe):
        log2_fc_threshold = 0
        pval_threshold = 0.05

        results_df = diffed_dataframe

        results_df["significance"] = "NOT_SIGNIFICANT"
        results_df.loc[
            (results_df["log2FoldChange"] > log2_fc_threshold)
            & (results_df["padj"] < pval_threshold),
            "significance",
        ] = "UP"
        results_df.loc[
            (results_df["log2FoldChange"] < log2_fc_threshold)
            & (results_df["padj"] < pval_threshold),
            "significance",
        ] = "DOWN"

        return results_df
