document.addEventListener('DOMContentLoaded', function() {
  const uploadForm = document.getElementById('uploadForm');
  const fileInput = document.getElementById('fileInput');
  const configSection = document.getElementById('configSection');
  const vizType = document.getElementById('vizType');
  const xColumn = document.getElementById('xColumn');
  const yColumn = document.getElementById('yColumn');
  const zColumn = document.getElementById('zColumn');
  const zColumnGroup = document.getElementById('zColumnGroup');
  const visualization = document.getElementById('visualization');
  const plotOutput = document.getElementById('plotOutput');

  let currentFilename = '';

  fileInput.addEventListener('change', async function(e) {
      const file = e.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('file', file);

      try {
          const response = await fetch('/upload', {
              method: 'POST',
              body: formData
          });

          const data = await response.json();

          if (data.error) {
              alert(data.error);
              return;
          }

          // Store filename for later use
          currentFilename = data.filename;

          // Populate column selectors
          const columns = data.columns;
          [xColumn, yColumn, zColumn].forEach(select => {
              select.innerHTML = '<option value="">Select Column</option>';
              columns.forEach(column => {
                  const option = document.createElement('option');
                  option.value = column;
                  option.textContent = column;
                  select.appendChild(option);
              });
          });

          // Show configuration section
          configSection.classList.remove('hidden');

      } catch (error) {
          console.error('Error:', error);
          alert('Error uploading file');
      }
  });

  vizType.addEventListener('change', function() {
      zColumnGroup.style.display = 
          ['scatter3d'].includes(this.value) ? 'block' : 'none';
  });

  uploadForm.addEventListener('submit', async function(e) {
      e.preventDefault();

      const vizData = {
          filename: currentFilename,
          viz_type: vizType.value,
          x_column: xColumn.value,
          y_column: yColumn.value,
          z_column: zColumn.value
      };

      try {
          const response = await fetch('/visualize', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(vizData)
          });

          const data = await response.json();

          if (data.error) {
              alert(data.error);
              return;
          }

          // Show visualization container
          visualization.classList.remove('hidden');

          // Parse the plot data and create the visualization
          const plotData = JSON.parse(data.plot);
          Plotly.newPlot('plotOutput', plotData.data, plotData.layout);

      } catch (error) {
          console.error('Error:', error);
          alert('Error generating visualization');
      }
  });
});