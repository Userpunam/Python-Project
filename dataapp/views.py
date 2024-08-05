from django.shortcuts import render
from .forms import UploadFileForm
from .models import UploadedFile
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from django.conf import settings

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            instance = UploadedFile(file=uploaded_file)
            instance.save()
            
            # Process the file
            df = pd.read_csv(instance.file.path)
            # Perform data analysis
            analysis_results = perform_data_analysis(df)
            
            return render(request, 'dataapp/results.html', {
                'analysis_results': analysis_results,
                'dataframe': df.head().to_html(),
            })
    else:
        form = UploadFileForm()
    return render(request, 'dataapp/upload.html', {'form': form})

def perform_data_analysis(df):
    summary_stats = df.describe().to_html()
    return {
        'summary_stats': summary_stats,
    }

def perform_data_analysis(df):
    summary_stats = df.describe().to_html()
    missing_values = df.isnull().sum().to_frame(name='Missing Values').to_html()
    mean_values = df.mean().to_frame(name='Mean').to_html()
    median_values = df.median().to_frame(name='Median').to_html()
    std_values = df.std().to_frame(name='Standard Deviation').to_html()

     plots = []

    for column in df.select_dtypes(include=['float64', 'int64']).columns:
        plt.figure()
        sns.histplot(df[column].dropna(), kde=True)
        plot_path = os.path.join(settings.MEDIA_ROOT, f'{column}_histogram.png')
        plt.savefig(plot_path)
        plots.append(f'{settings.MEDIA_URL}{column}_histogram.png')


    return {
        'summary_stats': summary_stats,
        'missing_values': missing_values,
        'mean_values': mean_values,
        'median_values': median_values,
        'std_values': std_values,
    }