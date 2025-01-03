interface = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bioinformatics Interface</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white p-10">
  <div class="max-w-2xl mx-auto bg-white shadow-md rounded-lg p-6 border">
    <h1 class="text-2xl font-bold text-[#42B0EC] mb-6">FunExpression</h1>
    <form id="bioform">
      <!-- Name -->
      <label class="block text-sm text-[#5BCFC1] mb-2" for="name">Name</label>
      <input class="w-full p-2 border border-[#76F191] rounded mb-4" type="text" id="name" name="name" placeholder="Enter name" required pattern="^[^0-9]+$">

      <!-- Email -->
      <label class="block text-sm text-[#5BCFC1] mb-2" for="email">Email</label>
      <input class="w-full p-2 border border-[#76F191] rounded mb-4" type="email" id="email" name="email" placeholder="Enter email" required>

      <!-- Reference Genome -->
      <label class="block text-sm text-[#5BCFC1] mb-2" for="reference_genome">Reference Genome Accession Number</label>
      <input class="w-full p-2 border border-[#76F191] rounded mb-4" type="text" id="reference_genome" name="reference_genome" placeholder="GCA_000346795.1" required>

      <!-- Control Sample (triplicate) -->
      <fieldset class="mb-6">
        <legend class="text-sm text-[#5BCFC1] mb-2">Control Sample (triplicate)</legend>
        <div class="flex gap-4">
          <input class="w-full p-2 border border-[#76F191] rounded" type="text" id="control_srr_1" name="control_srr_1" placeholder="SRR10042980" >
          <input class="w-full p-2 border border-[#76F191] rounded" type="text" id="control_srr_2" name="control_srr_2" placeholder="SRR10042981" >
          <input class="w-full p-2 border border-[#76F191] rounded" type="text" id="control_srr_3" name="control_srr_3" placeholder="SRR10042982" >
        </div>
      </fieldset>

      <!-- Experiment Sample (triplicate) -->
      <fieldset class="mb-6">
        <legend class="text-sm text-[#5BCFC1] mb-2">Experiment Sample (triplicate)</legend>
        <div class="flex gap-4">
          <input class="w-full p-2 border border-[#76F191] rounded" type="text" id="experiment_srr_1" name="experiment_srr_1" placeholder="SRR10042986" >
          <input class="w-full p-2 border border-[#76F191] rounded" type="text" id="experiment_srr_2" name="experiment_srr_2" placeholder="SRR10042987" >
          <input class="w-full p-2 border border-[#76F191] rounded" type="text" id="experiment_srr_3" name="experiment_srr_3" placeholder="SRR10042988" >
        </div>
      </fieldset>

      <!-- p_adj -->
      <label class="block text-sm text-[#5BCFC1] mb-2" for="p_adj">Padj</label>
      <input class="w-full p-2 border border-[#76F191] rounded mb-4" type="text" id="p_adj" name="p_adj" placeholder="0.05" required>

      <!-- Log2_Fold_Change_Threshold -->
      <label class="block text-sm text-[#5BCFC1] mb-2" for="log_2_fc">Log2 Fold Change Threshold</label>
      <input class="w-full p-2 border border-[#76F191] rounded mb-6" type="text" id="log_2_fc" name="log_2_fc" step="0.01" placeholder="2" required>

      <!-- Submit -->
      <button type="submit" class="w-full bg-[#42B0EC] text-white p-2 rounded">Submit</button>
    </form>
  </div>


  <script>
    document.getElementById('bioform').addEventListener('submit', async function(event) {
      event.preventDefault(); // Impede o envio padrão do formulário

      const data = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        control_organism: {
          srr_acession_number_1: document.getElementById('control_srr_1').value,
          srr_acession_number_2: document.getElementById('control_srr_2').value,
          srr_acession_number_3: document.getElementById('control_srr_3').value
        },
        experiment_organism: {
          srr_acession_number_1: document.getElementById('experiment_srr_1').value,
          srr_acession_number_2: document.getElementById('experiment_srr_2').value,
          srr_acession_number_3: document.getElementById('experiment_srr_3').value
        },
        reference_genome_acession_number: document.getElementById('reference_genome').value,
        p_adj: parseFloat(document.getElementById('p_adj').value),
        log_2_fold_change_threshold: parseFloat(document.getElementById('log_2_fc').value)
      };

      try {
        const response = await fetch("http://localhost/expression/calculate/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();
        console.log("Response:", result);
        alert("Sua solicitação foi recebida, você receberá os resultados no seu e-mail!");
      } catch (error) {
        console.error("Error:", error);
        alert("An error occurred during submission.");
      }
    });
  </script>

</body>
</html>

"""
