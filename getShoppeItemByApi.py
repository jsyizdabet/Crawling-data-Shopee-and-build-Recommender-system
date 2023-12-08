import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd

chrome_driver_path = r'"D:\Study/UEL/HK5/PHÂN TÍCH DỮ LIỆU WEB/crawlData/crawlData/chromedriver-win64/chromedriver-win64/chromedriver.exe"'

fileNameBackupCsv = 'data_backup'
fileNameBackupJson = 'data_backup'
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# api = 'https://shopee.vn/api/v4/recommend/recommend?bundle=category_landing_page&cat_level=1&catid=11035639&limit=5&offset=0'
api = 'https://shopee.vn/api/v4/recommend/recommend?bundle=category_landing_page&cat_level=1&catid=11035639&limit=500000&offset=0'
# api = 'https://viblo.asia/api/suggestion/service?type=viblo-ctf'

response = requests.get(api)

if response.status_code == 200:
    data = response.json()
    print('lay api thanh cong')
    list_item = data['data']['sections'][0]['data']['item']
    print('lay data thanh cong')
    # with open(fileNameBackupJson, 'w') as json_file:
    # json.dump(list_item, json_file)
   
    df = pd.DataFrame(list_item)
    print('convert sang df thanh cong')
    print(df.head)
    # Danh sách các cột muốn xóa
    columns_to_drop = [
    'shopid', 
    'itemid',
    'label_ids',
    'catid',
    'hidden_price_display',
    'has_lowest_price_guarantee',
    'is_category_failed',
    'size_chart',
    'video_info_list', 
    'reference_item_id',
    'transparent_background_image',
    'is_adult',
    'badge_icon_type',
    'shopee_verified',
    'is_official_shop',
    'show_official_shop_label',
    'show_shopee_verified_label',
    'show_official_shop_label_in_title',
    'is_cc_installment_payment_eligible',
    'is_non_cc_installment_payment_eligible',
    'coin_earn_label',
    'show_free_shipping',
    'preview_info',
    'coin_info',
    'exclusive_price_info',
    'bundle_deal_id',
     'is_group_buy_item',
    'has_group_buy_stock',
    'group_buy_info',
    'welcome_package_type',
    'welcome_package_info',
    'can_use_wholesale',
    'is_preferred_plus_seller',
    'has_model_with_available_shopee_stock',
    'is_on_flash_sale',
    'spl_installment_tenure',
    'is_live_streaming_price',
    'is_mart',
    'pack_size',
    'overlay_image',
    'autogen_title',
    'autogen_title_id',
    'overlay_id',
    'is_service_by_shopee',
    'free_shipping_info',
    'global_sold_count',
    'repurchase_rate',
    'best_selling_tag',
    'is_seller_configured',
    'tp_label',
    'flash_sale_design_style',
    'flash_sale_label_content',
    'flash_sale_sold_percentage',
    'info',
    'data_type',
    'key',
    'count',
    'adsid',
    'campaignid',
    'deduction_info',
    'video_display_control',
    'deep_discount_skin',
    'experiment_info',
    'relationship_label',
    'live_stream_session',
    'live_streaming_info',
    'new_user_label',
    'wp_eligibility',
    'platform_voucher',
    'rcmd_reason',
    'highlight_video',
    'can_use_cod',
    'pub_id',
    'pub_context_id',
    'friend_relationship_label',
    'showing_rs_label',
    'showing_friend_rs_label',
    'show_flash_sale_label',
    'search_id',
    'ext_info',
    'session_id',
    'algo_info',
    'hostid',
    'from',
    'view_cnt',
    'cover',
    'title',
    'avatar',
    'user_name',
    'play_url',
    'has_voucher',
    'has_draw',
    'draw_type',
    'has_streaming_price',
    'coins_per_claim',
    'play_url_expiration',
    'coins_can_claim_cnt',
    'item',
    'ui_type',
    'room_id',
    'user_id',
    'nick_name',
    'product_banners',
    'top_product_label',
    'fashion_item',
    'image_search',
    'generic_search_card'
    ]
   
    # Xóa các cột từ DataFrame
    df = df.drop(columns=columns_to_drop, axis=1)
    print('drop thanh cong')
    # lưu cái file excel cho chắc chứ lát shoppe ban thì bỏ mẹ
    excel_file_path = 'output.xlsx'
    df.to_excel(excel_file_path, index=False)
    
else:
    print('Request failed with status code:', response.status_code)

driver.quit()
