import streamlit as st

from dotenv import load_dotenv
load_dotenv()

import os
from autodesk_forge_sdk import OSSClient, OAuthTokenProvider

ossClient = OSSClient(OAuthTokenProvider(os.environ["FORGE_CLIENT_ID"], os.environ["FORGE_CLIENT_SECRET"]))

buckets = ossClient.get_all_buckets()

if 'bucket' not in st.session_state:
    st.session_state['bucket'] = ''

if 'object' not in st.session_state:
    st.session_state['object'] = ''

st.title("Autodesk Forge - Streamlite example")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Buckets")
    for bucket in buckets:
        bucketKey = bucket["bucketKey"]
        if st.button(bucketKey):
            st.session_state['bucket'] = bucketKey
with col2:
    st.subheader("Objects")
    if st.session_state['bucket'] != '' :
        objects = ossClient.get_all_objects(st.session_state['bucket'])

        if not objects :
            st.write('No objects in this bucket')
        for object in objects :
            objectKey = object["objectKey"]
            if st.button(objectKey):
                st.session_state['object'] = objectKey

with col3:
    st.subheader('Details')
    if st.session_state['bucket'] != '' and st.session_state['object'] != '':
        bucketKey = st.session_state['bucket']
        objectKey = st.session_state['object']
        details = ossClient.get_object_details(bucketKey, objectKey)
        st.write(f"Name: {details['objectKey']}")
        st.write(f"Size: {details['size']}")
        st.write(f"Location: {details['location']}")
        st.write(f"SHA1: {details['sha1']}")
