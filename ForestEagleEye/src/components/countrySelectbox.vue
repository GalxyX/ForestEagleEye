<template>
  <el-select v-model="value" placeholder="请选择国家和地区" popper-class="dropdown" style="width: 500px"
    @change="handleSelectChange">
    <el-option-group v-for="group in options" :key="group.label" :label="group.label">
      <el-option v-for="item in group.options" :key="item.iso" :label="item.name" :value="item.iso" />
    </el-option-group>
  </el-select>
</template>

<script lang="ts" setup>
import { ref, defineEmits } from 'vue'

const value = ref('CHN')

const options = [
  {
    label: 'A',
    options: [
      { name: 'Afghanistan', iso: 'AFG' },
      { name: 'Akrotiri and Dhekelia', iso: 'XAD' },
      { name: 'Albania', iso: 'ALB' },
      { name: 'Algeria', iso: 'DZA' },
      { name: 'American Samoa', iso: 'ASM' },
      { name: 'Andorra', iso: 'AND' },
      { name: 'Angola', iso: 'AGO' },
      { name: 'Anguilla', iso: 'AIA' },
      { name: 'Antarctica', iso: 'ATA' },
      { name: 'Antigua and Barbuda', iso: 'ATG' },
      { name: 'Argentina', iso: 'ARG' },
      { name: 'Armenia', iso: 'ARM' },
      { name: 'Aruba', iso: 'ABW' },
      { name: 'Australia', iso: 'AUS' },
      { name: 'Austria', iso: 'AUT' },
      { name: 'Azerbaijan', iso: 'AZE' },
    ],
  },
  {
    label: 'B',
    options: [
      { name: 'Bahamas', iso: 'Bahamas' },
      { name: 'Bahamas', iso: 'BHS' },
      { name: 'Bahrain', iso: 'BHR' },
      { name: 'Bangladesh', iso: 'BGD' },
      { name: 'Barbados', iso: 'BRB' },
      { name: 'Belarus', iso: 'BLR' },
      { name: 'Belgium', iso: 'BEL' },
      { name: 'Belize', iso: 'BLZ' },
      { name: 'Benin', iso: 'BEN' },
      { name: 'Bermuda', iso: 'BMU' },
      { name: 'Bhutan', iso: 'BTN' },
      { name: 'Bolivia', iso: 'BOL' },
      { name: 'Bonaire, Saint Eustatius and Saba', iso: 'BES' },
      { name: 'Bosnia and Herzegovina', iso: 'BIH' },
      { name: 'Botswana', iso: 'BWA' },
      { name: 'Bouvet Island', iso: 'BVT' },
      { name: 'Brazil', iso: 'BRA' },
      { name: 'British Indian Ocean Territory', iso: 'IOT' },
      { name: 'British Virgin Islands', iso: 'VGB' },
      { name: 'Brunei', iso: 'BRN' },
      { name: 'Bulgaria', iso: 'BGR' },
      { name: 'Burkina Faso', iso: 'BFA' },
      { name: 'Burundi', iso: 'BDI' },
    ],
  },
  {
    label: 'C',
    options: [
      { name: 'Cambodia', iso: 'KHM' },
      { name: 'Cameroon', iso: 'CMR' },
      { name: 'Canada', iso: 'CAN' },
      { name: 'Cape Verde', iso: 'CPV' },
      { name: 'Cayman Islands', iso: 'CYM' },
      { name: 'Central African Republic', iso: 'CAF' },
      { name: 'Chad', iso: 'TCD' },
      { name: 'Chile', iso: 'CHL' },
      { name: 'China', iso: 'CHN' },
      { name: 'Christmas Island', iso: 'CXR' },
      { name: 'Clipperton Island', iso: 'XCL' },
      { name: 'Cocos Islands', iso: 'CCK' },
      { name: 'Colombia', iso: 'COL' },
      { name: 'Comoros', iso: 'COM' },
      { name: 'Cook Islands', iso: 'COK' },
      { name: 'Costa Rica', iso: 'CRI' },
      { name: 'Croatia', iso: 'HRV' },
      { name: 'Cuba', iso: 'CUB' },
      { name: 'Curaçao', iso: 'CUW' },
      { name: 'Cyprus', iso: 'CYP' },
      { name: 'Czech Republic', iso: 'CZE' },
      { name: "Côte d'Ivoire", iso: 'CIV' },
    ],
  },
  {
    label: 'D',
    options: [
      { name: 'Democratic Republic of the Congo', iso: 'COD' },
      { name: 'Denmark', iso: 'DNK' },
      { name: 'Djibouti', iso: 'DJI' },
      { name: 'Dominica', iso: 'DMA' },
      { name: 'Dominican Republic', iso: 'DOM' },
    ],
  },
  {
    label: 'E',
    options: [
      { name: 'East Timor', iso: 'TLS' },
      { name: 'Ecuador', iso: 'ECU' },
      { name: 'Egypt', iso: 'EGY' },
      { name: 'El Salvador', iso: 'SLV' },
      { name: 'Equatorial Guinea', iso: 'GNQ' },
      { name: 'Eritrea', iso: 'ERI' },
      { name: 'Estonia', iso: 'EST' },
      { name: 'Ethiopia', iso: 'ETH' },
    ],
  },
  {
    label: 'F',
    options: [
      { name: 'Falkland Islands', iso: 'FLK' },
      { name: 'Faroe Islands', iso: 'FRO' },
      { name: 'Fiji', iso: 'FJI' },
      { name: 'Finland', iso: 'FIN' },
      { name: 'France', iso: 'FRA' },
      { name: 'French Guiana', iso: 'GUF' },
      { name: 'French Polynesia', iso: 'PYF' },
      { name: 'French Southern Territories', iso: 'ATF' },
    ],
  },
  {
    label: 'G',
    options: [
      { name: 'Gabon', iso: 'GAB' },
      { name: 'Gambia', iso: 'GMB' },
      { name: 'Georgia', iso: 'GEO' },
      { name: 'Germany', iso: 'DEU' },
      { name: 'Ghana', iso: 'GHA' },
      { name: 'Gibraltar', iso: 'GIB' },
      { name: 'Greece', iso: 'GRC' },
      { name: 'Greenland', iso: 'GRL' },
      { name: 'Grenada', iso: 'GRD' },
      { name: 'Guadeloupe', iso: 'GLP' },
      { name: 'Guam', iso: 'GUM' },
      { name: 'Guatemala', iso: 'GTM' },
      { name: 'Guernsey', iso: 'GGY' },
      { name: 'Guinea', iso: 'GIN' },
      { name: 'Guinea-Bissau', iso: 'GNB' },
      { name: 'Guyana', iso: 'GUY' },
    ],
  },
  {
    label: 'H',
    options: [
      { name: 'Haiti', iso: 'HTI' },
      { name: 'Heard Island and McDonald Islands', iso: 'HMD' },
      { name: 'Honduras', iso: 'HND' },
      { name: 'Hong Kong', iso: 'HKG' },
      { name: 'Hungary', iso: 'HUN' },
    ],
  },
  {
    label: 'I',
    options: [
      { name: 'Iceland', iso: 'ISL' },
      { name: 'India', iso: 'IND' },
      { name: 'Indonesia', iso: 'IDN' },
      { name: 'Iran', iso: 'IRN' },
      { name: 'Iraq', iso: 'IRQ' },
      { name: 'Ireland', iso: 'IRL' },
      { name: 'Isle of Man', iso: 'IMN' },
      { name: 'Israel', iso: 'ISR' },
      { name: 'Italy', iso: 'ITA' },
    ],
  },
  {
    label: 'J',
    options: [
      { name: 'Jamaica', iso: 'JAM' },
      { name: 'Japan', iso: 'JPN' },
      { name: 'Jersey', iso: 'JEY' },
      { name: 'Jordan', iso: 'JOR' },
    ],
  },
  {
    label: 'K',
    options: [
      { name: 'Kazakhstan', iso: 'KAZ' },
      { name: 'Kenya', iso: 'KEN' },
      { name: 'Kiribati', iso: 'KIR' },
      { name: 'Kosovo', iso: 'XKO' },
      { name: 'Kuwait', iso: 'KWT' },
      { name: 'Kyrgyzstan', iso: 'KGZ' },
    ],
  },
  {
    label: 'L',
    options: [
      { name: 'Laos', iso: 'LAO' },
      { name: 'Latvia', iso: 'LVA' },
      { name: 'Lebanon', iso: 'LBN' },
      { name: 'Lesotho', iso: 'LSO' },
      { name: 'Liberia', iso: 'LBR' },
      { name: 'Libya', iso: 'LBY' },
      { name: 'Liechtenstein', iso: 'LIE' },
      { name: 'Lithuania', iso: 'LTU' },
      { name: 'Luxembourg', iso: 'LUX' },
    ],
  },
  {
    label: 'M',
    options: [
      { name: 'Macao', iso: 'MAC' },
      { name: 'Macedonia', iso: 'MKD' },
      { name: 'Madagascar', iso: 'MDG' },
      { name: 'Malawi', iso: 'MWI' },
      { name: 'Malaysia', iso: 'MYS' },
      { name: 'Maldives', iso: 'MDV' },
      { name: 'Mali', iso: 'MLI' },
      { name: 'Malta', iso: 'MLT' },
      { name: 'Marshall Islands', iso: 'MHL' },
      { name: 'Martinique', iso: 'MTQ' },
      { name: 'Mauritania', iso: 'MRT' },
      { name: 'Mauritius', iso: 'MUS' },
      { name: 'Mayotte', iso: 'MYT' },
      { name: 'Mexico', iso: 'MEX' },
      { name: 'Micronesia', iso: 'FSM' },
      { name: 'Moldova', iso: 'MDA' },
      { name: 'Monaco', iso: 'MCO' },
      { name: 'Mongolia', iso: 'MNG' },
      { name: 'Montenegro', iso: 'MNE' },
      { name: 'Montserrat', iso: 'MSR' },
      { name: 'Morocco', iso: 'MAR' },
      { name: 'Mozambique', iso: 'MOZ' },
      { name: 'Myanmar', iso: 'MMR' },
    ],
  },
  {
    label: 'N',
    options: [
      { name: 'Namibia', iso: 'NAM' },
      { name: 'Nauru', iso: 'NRU' },
      { name: 'Nepal', iso: 'NPL' },
      { name: 'Netherlands', iso: 'NLD' },
      { name: 'New Caledonia', iso: 'NCL' },
      { name: 'New Zealand', iso: 'NZL' },
      { name: 'Nicaragua', iso: 'NIC' },
      { name: 'Niger', iso: 'NER' },
      { name: 'Nigeria', iso: 'NGA' },
      { name: 'Niue', iso: 'NIU' },
      { name: 'Norfolk Island', iso: 'NFK' },
      { name: 'North Korea', iso: 'PRK' },
      { name: 'Northern Cyprus', iso: 'XNC' },
      { name: 'Northern Mariana Islands', iso: 'MNP' },
      { name: 'Norway', iso: 'NOR' },
    ],
  },
  {
    label: 'O',
    options: [
      { name: 'Oman', iso: 'OMN' },
    ],
  },
  {
    label: 'P',
    options: [
      { name: 'Pakistan', iso: 'PAK' },
      { name: 'Palau', iso: 'PLW' },
      { name: 'Palestina', iso: 'PSE' },
      { name: 'Panama', iso: 'PAN' },
      { name: 'Papua New Guinea', iso: 'PNG' },
      { name: 'Paraguay', iso: 'PRY' },
      { name: 'Peru', iso: 'PER' },
      { name: 'Philippines', iso: 'PHL' },
      { name: 'Pitcairn Islands', iso: 'PCN' },
      { name: 'Poland', iso: 'POL' },
      { name: 'Portugal', iso: 'PRT' },
      { name: 'Puerto Rico', iso: 'PRI' },
    ],
  },
  {
    label: 'Q',
    options: [
      { name: 'Qatar', iso: 'QAT' },
    ],
  },
  {
    label: 'R',
    options: [
      { name: 'Republic of Congo', iso: 'COG' },
      { name: 'Reunion', iso: 'REU' },
      { name: 'Romania', iso: 'ROU' },
      { name: 'Russia', iso: 'RUS' },
      { name: 'Rwanda', iso: 'RWA' },
    ],
  },
  {
    label: 'S',
    options: [
      { name: 'Saint Helena', iso: 'SHN' },
      { name: 'Saint Kitts and Nevis', iso: 'KNA' },
      { name: 'Saint Lucia', iso: 'LCA' },
      { name: 'Saint Pierre and Miquelon', iso: 'SPM' },
      { name: 'Saint Vincent and the Grenadines', iso: 'VCT' },
      { name: 'Saint-Barthélemy', iso: 'BLM' },
      { name: 'Saint-Martin', iso: 'MAF' },
      { name: 'Samoa', iso: 'WSM' },
      { name: 'San Marino', iso: 'SMR' },
      { name: 'Sao Tome and Principe', iso: 'STP' },
      { name: 'Saudi Arabia', iso: 'SAU' },
      { name: 'Senegal', iso: 'SEN' },
      { name: 'Serbia', iso: 'SRB' },
      { name: 'Seychelles', iso: 'SYC' },
      { name: 'Sierra Leone', iso: 'SLE' },
      { name: 'Singapore', iso: 'SGP' },
      { name: 'Sint Maarten', iso: 'SXM' },
      { name: 'Slovakia', iso: 'SVK' },
      { name: 'Slovenia', iso: 'SVN' },
      { name: 'Solomon Islands', iso: 'SLB' },
      { name: 'Somalia', iso: 'SOM' },
      { name: 'South Africa', iso: 'ZAF' },
      { name: 'South Georgia and the South Sandwich Islands', iso: 'SGS' },
      { name: 'South Korea', iso: 'KOR' },
      { name: 'South Sudan', iso: 'SSD' },
      { name: 'Spain', iso: 'ESP' },
      { name: 'Sri Lanka', iso: 'LKA' },
      { name: 'Sudan', iso: 'SDN' },
      { name: 'Suriname', iso: 'SUR' },
      { name: 'Svalbard and Jan Mayen', iso: 'SJM' },
      { name: 'Swaziland', iso: 'SWZ' },
      { name: 'Sweden', iso: 'SWE' },
      { name: 'Switzerland', iso: 'CHE' },
      { name: 'Syria', iso: 'SYR' },
    ],
  },
  {
    label: 'T',
    options: [
      { name: 'Tajikistan', iso: 'TJK' },
      { name: 'Tanzania', iso: 'TZA' },
      { name: 'Thailand', iso: 'THA' },
      { name: 'Togo', iso: 'TGO' },
      { name: 'Tokelau', iso: 'TKL' },
      { name: 'Tonga', iso: 'TON' },
      { name: 'Trinidad and Tobago', iso: 'TTO' },
      { name: 'Tunisia', iso: 'TUN' },
      { name: 'Turkey', iso: 'TUR' },
      { name: 'Turkmenistan', iso: 'TKM' },
      { name: 'Turks and Caicos Islands', iso: 'TCA' },
      { name: 'Tuvalu', iso: 'TUV' },
    ],
  },
  {
    label: 'U',
    options: [
      { name: 'Uganda', iso: 'UGA' },
      { name: 'Ukraine', iso: 'UKR' },
      { name: 'United Arab Emirates', iso: 'ARE' },
      { name: 'United Kingdom', iso: 'GBR' },
      { name: 'United States', iso: 'USA' },
      { name: 'United States Minor Outlying Islands', iso: 'UMI' },
      { name: 'Uruguay', iso: 'URY' },
    ],
  },
  {
    label: 'V',
    options: [
      { name: 'Vanuatu', iso: 'VUT' },
      { name: 'Vatican City', iso: 'VAT' },
      { name: 'Venezuela', iso: 'VEN' },
      { name: 'Vietnam', iso: 'VNM' },
      { name: 'Virgin Islands, U.S.', iso: 'VIR' },
    ],
  },
  {
    label: 'W',
    options: [
      { name: 'Wallis and Futuna', iso: 'WLF' },
      { name: 'Western Sahara', iso: 'ESH' },
    ],
  },
  {
    label: 'Y',
    options: [
      { name: 'Yemen', iso: 'YEM' },
    ],
  },
  {
    label: 'Z',
    options: [
      { name: 'Zambia', iso: 'Zambia' },
      { name: 'Zimbabwe', iso: 'Zimbabwe' },
    ],
  },
]

const emit = defineEmits(['select-change'])
function handleSelectChange(value: any) {
  emit('select-change', value)
}
</script>

<style>
.el-select-dropdown__item.selected {
  color: green !important;
}

.dropdown {
  background-color: #fff;
  color: #333;
  font-size: 14px;
  padding: 8px 12px;
  box-sizing: border-box;
  z-index: 99999 !important;
}

.dropdown .el-select-dropdown__item {
  color: grey;
}

.dropdown .el-select-dropdown__item.hover,
.dropdown .el-select-dropdown__item:hover {
  background-color: rgba(149, 242, 4, 0.01);
  box-shadow: 0px 0px 78px rgba(149, 242, 4, 0.1) inset;
  color: #60a103;
}
</style>