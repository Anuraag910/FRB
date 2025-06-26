import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

Team_Name = input("Team_Name = ")
csv_file = rf"/home/czti/user_area/anuraag/FRB_report/frb_db_{Team_Name}.csv"  
df = pd.read_csv(csv_file)
base_path = rf"/home/czti/user_area/anuraag/FRB_report/FRB_team_{Team_Name}"

# Add columns for flux limits and fluence
df['Comment'] = "Observed" 
df['FluxLimit(1e-6)_tbin_0.01'] = "None"
df['FluxLimit(1e-6)_tbin_0.1'] = "None"
df['FluxLimit(1e-6)_tbin_1.0'] = "None"
df['Fluence(1e-6)_tbin_0.01'] = "None"
df['Fluence(1e-6)_tbin_0.1'] = "None"
df['Fluence(1e-6)_tbin_1.0'] = "None"

for idx, row in df.iterrows():
    name = row['Name']
    flux_file_path = os.path.join(base_path, name, "Products", f"{name}_Fluxlimits_-1.txt")
    SAA = os.path.join(base_path, name, f"{name}_SAA_strikes_again.txt")
    EO = os.path.join(base_path,name,"Products",f"{name}_Angles_EO.txt")
    asimov = os.path.join(base_path, name,"asimov.png")
    
    # print(f"Row {idx}, Name: {name}")
    # print(f"  SAA exists: {os.path.exists(SAA)}")
    # print(f"  EO exists: {os.path.exists(EO)}")
    # print(f"  Asimov exists: {os.path.exists(asimov)}")
    # print(f"  Flux file exists: {os.path.exists(flux_file_path)}")
        
    
    
    
    
    # Update Comment column first
    if os.path.exists(SAA):
        df.at[idx, 'Comment'] = "In SAA"
    elif os.path.exists(EO):  
        df.at[idx, 'Comment'] = "Earth Occulted"
    elif os.path.exists(asimov):
        df.at[idx, 'Comment'] = "No orbit data"
    
    # Now handle the flux file
    if os.path.exists(flux_file_path):
        # Read the flux file
        flux_df = pd.read_csv(flux_file_path, delim_whitespace=True)
        
        # Extract and format flux values for specific tbin values
        flux_0_01 = flux_df.loc[flux_df['tbin'] == 0.01, 'Flux'].values
        flux_0_1 = flux_df.loc[flux_df['tbin'] == 0.1, 'Flux'].values
        flux_1_0 = flux_df.loc[flux_df['tbin'] == 1.0, 'Flux'].values
        
          # Calculate and assign flux and fluence values
        if len(flux_0_01) > 0:
            flux_value = flux_0_01[0]
            fluence_value = flux_value * 0.01
            df.at[idx, 'FluxLimit(1e-6)_tbin_0.01'] = f"{flux_value * 1e6}"
            df.at[idx, 'Fluence(1e-6)_tbin_0.01'] = f"{fluence_value * 1e6}"
        if len(flux_0_1) > 0:
            flux_value = flux_0_1[0]
            fluence_value = flux_value * 0.1
            df.at[idx, 'FluxLimit(1e-6)_tbin_0.1'] = f"{flux_value * 1e6}"
            df.at[idx, 'Fluence(1e-6)_tbin_0.1'] = f"{fluence_value * 1e6}"
        if len(flux_1_0) > 0:
            flux_value = flux_1_0[0]
            fluence_value = flux_value * 1.0
            df.at[idx, 'FluxLimit(1e-6)_tbin_1.0'] = f"{flux_value * 1e6}"
            df.at[idx, 'Fluence(1e-6)_tbin_1.0'] = f"{fluence_value * 1e6}"


output_csv_path = f"/home/czti/user_area/anuraag/FRB_report/FRB_team_{Team_Name}_with_flux_and_fluence.csv"  
df.to_csv(output_csv_path, index=False)

print(f"Updated CSV file saved to {output_csv_path}")

# Plot histograms for flux
flux_0_01 = pd.to_numeric(df['FluxLimit(1e-6)_tbin_0.01'], errors='coerce').dropna()
flux_0_1 = pd.to_numeric(df['FluxLimit(1e-6)_tbin_0.1'], errors='coerce').dropna()
flux_1_0 = pd.to_numeric(df['FluxLimit(1e-6)_tbin_1.0'], errors='coerce').dropna()

#lux_1_0  = df['Fluence(1e-6)_tbin_1.0'].values
# [print("########", val) for val in df['FluxLimit(1e-6)_tbin_0.01'].values]
# print("@@@@@@@",pd.to_numeric(df['FluxLimit(1e-6)_tbin_0.01'], errors='coerce'))
 
plt.figure(figsize=(10, 6))
bins = 10**np.linspace(-1, 1.5,10)
print("Length heyo", len(flux_0_01))
plt.hist(flux_0_01, bins=bins, histtype='step', alpha=0.5, label='tbin = 0.01', color='blue')
plt.hist(flux_0_1, bins=bins, histtype='step', alpha=0.5, label='tbin = 0.1', color='green')
plt.hist(flux_1_0, bins=bins, histtype='step', alpha=0.5, label='tbin = 1.0', color='red')

plt.xscale('log')
plt.title(f'Team {Team_Name} Flux Histogram at Different Time Bins', fontsize=16)
plt.xlabel('X-ray Flux Limit (x$10^{-6}$)', fontsize=14)
plt.ylabel('FRBs', fontsize=14)
plt.legend(fontsize=12)
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(f"/home/czti/user_area/anuraag/FRB_report/Flux_limit_histogram_FRBs{Team_Name}.png", dpi=300)
print(f"Plot saved to /home/czti/user_area/anuraag/FRB_report/Flux_limit_histogram_FRBs{Team_Name}.png")

# Plotting the fluence histograms
Bins = 10**np.linspace(-2, 1,10)
plt.figure(figsize=(10, 6))
plt.hist(flux_0_01*0.01, bins=Bins,histtype='step', alpha=0.5, label='tbin = 0.01', color='blue')
plt.hist(flux_0_1*0.1, bins=Bins, histtype='step',alpha=0.5, label='tbin = 0.1', color='green')
plt.hist(flux_1_0*1.0, bins=Bins, histtype='step',alpha=0.5, label='tbin = 1.0', color='red')

plt.xscale('log')
# Adding labels and legend
plt.title(f'Team {Team_Name} Fluence Histogram at Different Time Bins', fontsize=16)
plt.xlabel('X-ray Fluence Limit (x$10^{-6}$)', fontsize=14)
plt.ylabel('FRBs', fontsize=14)
plt.legend(fontsize=12)
plt.grid(alpha=0.3)

# Show the plot
plt.tight_layout()
plt.savefig(f"/home/czti/user_area/anuraag/FRB_report/Fluence_limit_histogram_FRBs{Team_Name}", dpi=300)  # Save the figure with high resolution
print(f"Plot saved to /home/czti/user_area/anuraag/FRB_report/Fluence_limit_histogram_FRBs{Team_Name}.png")

comment_counts = df['Comment'].value_counts()
labels = comment_counts.index
sizes = comment_counts.values

# Generate the pie chart
plt.figure(figsize=(8, 8))
plt.tight_layout()
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title(f" Team Name: {Team_Name}")
plt.legend(title=f"Total Source = {len(df['Comment'])}", loc="lower right")
pie_chart_path = f"/home/czti/user_area/anuraag/FRB_report/Observed_FRBs_{Team_Name}_pie_chart.png"
plt.savefig(pie_chart_path, dpi=300)
plt.show()

print(f"Pie chart saved to {pie_chart_path}")