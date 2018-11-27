import base64
import codecs


def encrypt(source_file, target_file):
    with codecs.open(source_file, 'r') as sf:
        text = sf.read()

    with codecs.open(target_file, 'w+b') as tf:
        tf.write(base64.encodestring(text))

    return text


def decrypt(source_file, target_file):
    with codecs.open(source_file, 'r') as sf:
        text = sf.read()

    with codecs.open(target_file, 'w+b') as tf:
        tf.write(base64.decodestring(text))

    return text


if __name__ == '__main__':
    source = "../config/source.properties"
    target = "../config/target.properties"

    # encrypt(source, target)

    # decrypt(target, source)
