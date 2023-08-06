sheet_name = "MEA dashboard"
google_cred = "./credentials/vibrant-epsilon-169702-467fddc26dfc.json"
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

#### parameters for low pass filter
filter_pre_resample = 100
filter_post_resample = 10
filter_kernel_size = 51

# find centers
center_search_range = (6,6,6)

spike_bin_size = 5*20*1000 # unit us

